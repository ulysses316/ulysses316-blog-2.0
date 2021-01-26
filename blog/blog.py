import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app,
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from blog.auth import login_required
from .models import Post
from . import db
from flask_login import current_user
# AWS
import boto3, botocore

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('blog', __name__)

# Subir archivos

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_s3(s3, file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type    #Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(current_app.config["S3_LOCATION"], file.filename)

@bp.route('/blog')
def blog():
    posts = Post.query.order_by(Post.created)
    return render_template('blog/blog.html', posts=posts)

@bp.route('/post/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['ckeditor']
        file = request.files['file']


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
            file.filename = "blog/{}".format(secure_filename(file.filename))
        # AWS
            output = upload_file_to_s3(s3, file, current_app.config['S3_BUCKET'])
        # AWS

        new_post = Post(author_id=current_user.get_id(), title=title, body=body, file=str(output))
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog.blog'))

    return render_template('blog/create.html')


@bp.route('/post/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = Post.query.get(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['ckeditor']
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
            file.filename = "blog/{}".format(secure_filename(file.filename))
            output = upload_file_to_s3(s3, file, current_app.config['S3_BUCKET'])

        if not file:
            output = post.file

        post.title = title
        post.body = body
        post.file = output
        db.session.commit()
        return redirect(url_for('blog.blog'))

    return render_template('blog/update.html', post=post)

@bp.route('/post/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.blog'))


@bp.route('/post/<int:id>')
def post(id):
    post = Post.query.get(id)
    return render_template("blog/post.html", post=post)