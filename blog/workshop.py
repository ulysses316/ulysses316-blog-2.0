from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os
from flask_login import current_user
from .models import Workshop
from . import db
from .auth import login_required
# AWS
import boto3, botocore
from .blog import upload_file_to_s3

from blog.auth import login_required
from . import csrf

bp = Blueprint('workshop', __name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Subir archivos

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/workshops')
def workshop():
    workshops = Workshop.query.order_by(Workshop.created)
    return render_template('workshop/workshops.html', workshops=workshops)

@csrf.exempt
@bp.route('/workshop/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        url = request.form['url']
        file = request.files['file']
        error = None

        s3 = boto3.client(
            "s3",
            aws_access_key_id=current_app.config['S3_KEY'],
            aws_secret_access_key=current_app.config['S3_SECRET']
        )

        if 'file' not in request.files:
            error = 'No file part'
        if file.filename == '':
            error = 'No selected file'
        if file and allowed_file(file.filename):
            file.filename = "workshops/{}".format(secure_filename(file.filename))
            output = upload_file_to_s3(s3, file, current_app.config['S3_BUCKET'])
        if not title:
            error = 'Title is required.'

        workshop = Workshop(author_id=current_user.get_id() ,title=title, body=body, url=url, file=output)
        db.session.add(workshop)
        db.session.commit()

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('workshop.workshop'))

    return render_template('workshop/create.html')

@csrf.exempt
@bp.route('/workshop/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    workshops = Workshop.query.get(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        url = request.form['url']
        file = request.files['file']

        s3 = boto3.client(
            "s3",
            aws_access_key_id=current_app.config['S3_KEY'],
            aws_secret_access_key=current_app.config['S3_SECRET']
        )

        if file.filename == '':
            error = 'No selected file'
        if file and allowed_file(file.filename):
            file.filename = "workshops/{}".format(secure_filename(file.filename))
            output = upload_file_to_s3(s3, file, current_app.config['S3_BUCKET'])


        if not file:
            filename = workshops.file

        workshops.title = title
        workshops.body = body
        workshops.url = url
        workshops.file = output
        db.session.commit()

        return redirect(url_for('workshop.workshop'))

    return render_template('workshop/update.html', workshop=workshops)

@csrf.exempt
@bp.route('/workshop/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    workshop = Workshop.query.get(id)
    db.session.delete(workshop)
    db.session.commit()
    return redirect(url_for('workshop.workshop'))
