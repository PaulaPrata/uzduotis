import os
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from core import secrets


basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'uzduotis.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'register'
login_manager.login_message_category = 'info'

from flask_mail import Message, Mail


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'secrets.email'
app.config['MAIL_PASSWORD'] = 'secrets.password'

mail = Mail(app)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset form',
                  sender= secrets.email,
                  recipients=[user.email])
    msg.body = f'''If you would like to update your password, click here:
    {url_for('reset_token', token=token, _external=True)}
    If you haven't requested for a password update, ignore it and your password won't be updated.
    '''
    mail.send(msg)

from core import routes