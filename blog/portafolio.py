from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import requests
from werkzeug.exceptions import abort

from blog.auth import login_required

bp = Blueprint('portafolio', __name__)

@bp.route('/portafolio')
def portafolio():
    r = requests.get("https://api.github.com/users/ulysses316").json()
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
    return render_template('portafolio/create.html')

def get_projects(id, check_author=True):

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
            return redirect(url_for('portafolio.portafolio'))

    return render_template('portafolio/update.html', projects=projects)

@bp.route('/project/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_projects(id)
    return redirect(url_for('portafolio.portafolio'))