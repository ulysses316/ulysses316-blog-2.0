from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from blog.auth import login_required
from blog.db import get_db

bp = Blueprint('workshop', __name__)

@bp.route('/workshops')
def workshop():
    db = get_db()
    workshops = db.execute(
        'SELECT w.id, title, body, url'
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
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO workshops (title, body, url, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, url, g.user['id'])
            )
            db.commit()
            return redirect(url_for('workshop.workshop'))

    return render_template('workshop/create.html')

def get_workshops(id, check_author=True):
    workshop = get_db().execute(
        'SELECT w.id, title, body, url, created, author_id, username'
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
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE workshops SET title = ?, body = ?, url = ?'
                ' WHERE id = ?',
                (title, body, url, id)
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
