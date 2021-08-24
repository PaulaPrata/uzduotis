from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FloatField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
from core import app, models



class RegForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('password', [DataRequired()])
    confirm_email = PasswordField("Please repeat the password", [EqualTo('password', "Password has to match.")])
    submit = SubmitField('Register')

    def check_name(self, name):
        customer = app.Customers.query.filter_by(name=name.data).first()
        if customer:
            raise ValidationError('There is already a user with this user name. Please choose another')

    def check_name(self, email):
        customer = app.Customers.query.filter_by(el_pastas=email.data).first()
        if customer:
            raise ValidationError('There is already a user with this email. Please choose another.')

class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login in')

class RecordForm(FlaskForm):
    project_name = StringField('Project Name', [DataRequired()])
    submit = SubmitField('Submit')

# def folder_name_query():
#     return folder_name.query
#
# def project_name_query():
#     return project_name.query

class TaskForm(FlaskForm):
    task_name = StringField('Task Name', [DataRequired()])
    project = QuerySelectField("Project Name", query_factory=models.Projects.query.all, allow_blank=True, get_label='project_name', get_pk=lambda obj: str(obj))
    # folder_name = QuerySelectField("Folder Name", query_factory=, allow_blank=True, get_label='folder_name', get_pk=lambda obj: str(obj)
    submit = SubmitField('Submit')



