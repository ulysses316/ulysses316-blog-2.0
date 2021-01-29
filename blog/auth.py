# importaciones de flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# Importaciones de seguridad para hashear nuestra contraseña
from werkzeug.security import check_password_hash, generate_password_hash
# Importacion de flask login
from flask_login import login_user, logout_user, login_required
# importaciones locales de nuestro modelo usuario y nuestro objeto db
from .models import User
from . import db

from . import csrf
# Creamos nuestro Blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

@csrf.exempt
@bp.route('/register', methods=('GET', 'POST'))
@login_required
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        error = None

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Este correo ya esta registrado')
            return redirect(url_for('auth.register'))
        else:
            new_user = User(name=name, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@csrf.exempt
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        print(user)

        if not user or not check_password_hash(user.password, password):
            alert = 'danger'
            flash('Por favor vuelve a intentar')
            return redirect(url_for('auth.login'))
        else:
            flash('Iniciaste sesion')
            login_user(user)
        return redirect(url_for('index'))
    return render_template('auth/login.html')

@csrf.exempt
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))