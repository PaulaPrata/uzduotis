from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
from core import app, models
from wtforms.fields.html5 import DateField


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

    def check_email(self, email):
        customer = app.Customers.query.filter_by(email=email.data).first()
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


class TaskForm(FlaskForm):
    task_name = StringField('Task Name', [DataRequired()])
    status = SelectField('Completion status', choices=[('Active'), ('Completed')])
    project = QuerySelectField("Project Name", query_factory=models.Projects.query.all, allow_blank=True,
                               get_label='project_name', get_pk=lambda obj: str(obj))
    date = DateField('DatePicker', format='%Y-%m-%d')
    submit = SubmitField('Submit')


class TaskStatusUpdateForm(FlaskForm):
    status = SelectField('Completion status', choices=[('Active'), ('Completed')])
    submit = SubmitField('Submit')


class RequestUpdateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = models.Customers.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no user with this account with this email address. Register.')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirmed_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit Password')


class AccountUpdateForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    photo = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Submit')

    def check_name(self, name):
        if name.data != app.current_user.name:
            customer = app.Customers.query.filter_by(name=name.data).first()
            if customer:
                raise ValidationError('This name is used already, please choose another one.')

    def check_email(self, email):
        if email.data != app.current_user.email:
            customer = app.Vartotojas.query.filter_by(email=email.data).first()
            if customer:
                raise ValidationError('This email is used already, please choose another one.')
