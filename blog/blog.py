from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os

from blog.auth import login_required
from blog.db import get_db

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('blog', __name__)

# Subir archivos

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/blog')
def blog():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, file, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/blog.html', posts=posts)

@bp.route('/post/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        file = request.files['file']
        error = None

        if 'file' not in request.files:
            error = 'No file part'

        if file.filename == '':
            error = 'No selected file'
        if file and allowed_file(file.filename):
            filename = "blog/{}".format(secure_filename(file.filename))
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, file, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, filename, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.blog'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, file, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return post

@bp.route('/post/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        file = request.files['file']
        error = None

        if 'file' not in request.files:
            error = 'No file part'

        if file.filename == '':
            error = 'No selected file'
        if file and allowed_file(file.filename):
            filename = "blog/{}".format(secure_filename(file.filename))
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, file = ?'
                ' WHERE id = ?',
                (title, body, filename, id)
            )
            db.commit()
            return redirect(url_for('blog.blog'))

    return render_template('blog/update.html', post=post)

@bp.route('/post/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.blog'))

@bp.route('/post/<int:id>')
def post(id):
    post = get_post(id)
    return render_template("blog/post.html", post=post)