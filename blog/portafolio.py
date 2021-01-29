from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import requests
from werkzeug.exceptions import abort
from .models import Project
from . import db
from .auth import login_required
from flask_login import current_user
from blog.auth import login_required
from . import csrf

bp = Blueprint('portafolio', __name__)

@bp.route('/portafolio')
def portafolio():
    r = requests.get("https://api.github.com/users/ulysses316").json()
    projects = Project.query.order_by(Project.created)
    return render_template('portafolio/portafolio.html', r=r, projects=projects)

@csrf.exempt
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
        new_project = Project(author_id=current_user.get_id(), title=r['name'], body=r['description'], url=r['html_url'], language=r['language'])
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('portafolio.portafolio'))

    return render_template('portafolio/create.html')

@csrf.exempt
@bp.route('/project/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    projects = Project.query.get(id)
    if request.method == 'POST':
        urlRepo = request.form['urlRepo']
        r = requests.get("https://api.github.com/repos/{}".format(urlRepo))
        error = None
        if r.status_code != 200:
            error = 'Hubo un error en la peticion'
        r = r.json()

        projects.title= r['name']
        projects.body = r['description']
        projects.url = r['html_url']
        projects.language = r['language']
        db.session.commit()

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('portafolio.portafolio'))

    return render_template('portafolio/update.html', projects=projects)

@csrf.exempt
@bp.route('/project/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('portafolio.portafolio'))