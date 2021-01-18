from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import requests
from werkzeug.exceptions import abort

from blog.auth import login_required
from blog.db import get_db

bp = Blueprint('portafolio', __name__)

@bp.route('/portafolio')
def portafolio():
    r = requests.get("https://api.github.com/users/ulysses316").json()
    db = get_db()
    projects = db.execute(
        'SELECT p.id, title, description, url, language, created, author_id, username'
        ' FROM projects p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('portafolio/portafolio.html', r=r, projects=projects)

@bp.route('/portafolio/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        error = None
        urlRepo = request.form['urlRepo']
        r = requests.get("https://api.github.com/repos/{}".format(urlRepo))
        if r.status_code != 200:
            error = 'Hubo un error en la peticion'
        r = r.json()
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO projects (title, description, url, language, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (r['name'], r['description'],r['html_url'],r['language'], g.user['id'])
            )
            db.commit()
            return redirect(url_for('portafolio.portafolio'))

    return render_template('portafolio/create.html')

def get_projects(id, check_author=True):
    projects = get_db().execute(
        'SELECT p.id, title, description, url, language, created, author_id, username'
        ' FROM projects p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if projects is None:
        abort(404, "Projects id {0} doesn't exist.".format(id))

    return projects

@bp.route('/project/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    projects = get_projects(id)

    if request.method == 'POST':
        urlRepo = request.form['urlRepo']
        r = requests.get("https://api.github.com/repos/{}".format(urlRepo))
        error = None
        if r.status_code != 200:
            error = 'Hubo un error en la peticion'
        r = r.json()
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE projects SET title = ?, description = ?, url = ?, language = ?'
                ' WHERE id = ?',
                (r['name'], r['description'],r['html_url'],r['language'] , id)
            )
            db.commit()
            return redirect(url_for('portafolio.portafolio'))

    return render_template('portafolio/update.html', projects=projects)

@bp.route('/project/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_projects(id)
    db = get_db()
    db.execute('DELETE FROM projects WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('portafolio.portafolio'))