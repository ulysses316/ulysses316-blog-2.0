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

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('blog', __name__)

# Subir archivos

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/blog')
def blog():
    posts = Post.query.order_by(Post.created)
    return render_template('blog/blog.html', posts=posts)

@bp.route('/post/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        file = request.files['file']

        if 'file' not in request.files:
            error = 'No file part'
        if file.filename == '':
            error = 'No selected file'
        if file and allowed_file(file.filename):
            filename = "blog/{}".format(secure_filename(file.filename))
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        new_post = Post(author_id=current_user.get_id(), title=title, body=body, file=filename)
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

        if not file:
            filename = post.file

        post.title = title
        post.body = body
        post.file = filename
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