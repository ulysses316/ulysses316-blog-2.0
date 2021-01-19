from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app,
)
from flask_mail import Mail, Message

bp = Blueprint('email', __name__)


@bp.route("/email", methods=['GET', 'POST'])
def email():
    if request.method == 'POST':
        subject = request.form['subject']
        nameSender = request.form['nameSender']
        email = request.form['senderEmail']
        message = request.form['message']

        mail = Mail(current_app)
        msg = Message(subject, sender='joedoefirebase@gmail.com', recipients=['joedoefirebase@gmail.com','ulises316@live.com.mx', 'ulysses316.hugm@gmail.com'])
        msg.body = "{}\n\n{} - {}\n\n{}".format(subject, nameSender, email, message)
        mail.send(msg)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    return redirect(url_for('index'))