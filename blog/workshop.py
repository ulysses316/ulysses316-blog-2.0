from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os

from blog.auth import login_required
from blog.db import get_db

bp = Blueprint('workshop', __name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Subir archivos

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/workshops')
def workshop():
    db = get_db()
    workshops = db.execute(
        'SELECT w.id, title, body, url, file'
        ' FROM workshops w JOIN user u ON w.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('workshop/workshops.html', workshops=workshops)

@bp.route('/workshop/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        url = request.form['url']
        file = request.files['file']
        error = None

        if 'file' not in request.files:
            error = 'No file part'

        if file.filename == '':
            error = 'No selected file'
        if file and allowed_file(file.filename):
            filename = "workshop/{}".format(secure_filename(file.filename))
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO workshops (title, body, url, file, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, body, url, filename, g.user['id'])
            )
            db.commit()
            return redirect(url_for('workshop.workshop'))

    return render_template('workshop/create.html')

def get_workshops(id, check_author=True):
    workshop = get_db().execute(
        'SELECT w.id, title, body, url, file, created, author_id, username'
        ' FROM workshops w JOIN user u ON w.author_id = u.id'
        ' WHERE w.id = ?',
        (id,)
    ).fetchone()

    if workshop is None:
        abort(404, "Workshops id {0} doesn't exist.".format(id))

    return workshop

@bp.route('/workshop/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    workshops = get_workshops(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        url = request.form['url']
        file = request.files['file']
        error = None

        if 'file' not in request.files:
            error = 'No file part'

        if file.filename == '':
            error = 'No selected file'
        if file and allowed_file(file.filename):
            filename = "workshop/{}".format(secure_filename(file.filename))
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE workshops SET title = ?, body = ?, url = ?, file = ?'
                ' WHERE id = ?',
                (title, body, url, filename, id)
            )
            db.commit()
            return redirect(url_for('workshop.workshop'))

    return render_template('workshop/update.html', workshop=workshops)

@bp.route('/workshop/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_workshops(id)
    db = get_db()
    db.execute('DELETE FROM workshops WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('workshop.workshop'))
