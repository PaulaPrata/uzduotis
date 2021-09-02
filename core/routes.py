from flask import render_template, redirect, flash, url_for, request
from core import db, models, Bcrypt, login_manager, send_reset_email
from flask_login import current_user, login_user, logout_user, login_required
from core.models import Customers
from core import app, os
from core.forms import RegForm, LoginForm, RecordForm, TaskForm, TaskStatusUpdateForm, RequestUpdateForm, \
    PasswordResetForm, AccountUpdateForm
from datetime import datetime
import secrets
from PIL import Image

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@login_manager.user_loader
def load_user(id):
    return Customers.query.get(int(id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        customer = Customers(name=form.name.data, email=form.email.data,
                             password=hashed_password)
        db.session.add(customer)
        db.session.commit()
        flash('Sėkmingai prisiregistravote! Galite prisijungti', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Registracija', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.Customers.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login failed!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/records")
@login_required
def records():
    db.create_all()
    try:
        all_projects = models.Projects.query.filter_by(customer_id=current_user.id).all()
    except:
        all_projects = []
    print(all_projects)
    return render_template("records.html", all_projects=all_projects, datetime=datetime)


@app.route("/new_project", methods=["GET", "POST"])
@login_required
def new_project():
    db.create_all()
    form = RecordForm()
    if form.validate_on_submit():
        new_project = models.Projects(project_name=form.project_name.data, customer_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()
        flash(f"New Project is Created", 'success')
        return redirect(url_for('records'))
    return render_template("add_project.html", form=form)


@app.route("/new_task", methods=["GET", "POST"])
@login_required
def new_task():
    db.create_all()
    form = TaskForm()
    if form.validate_on_submit():
        new_task = models.Tasks(task_name=form.task_name.data, customer_id=current_user.id,
                                project_id=form.project.data.id, status=form.status.data, date=form.date.data)
        db.session.add(new_task)
        db.session.commit()
        flash(f"New Task is added to Project", 'success')
        return redirect(url_for('records'))
    return render_template("add_task.html", form=form)


@app.route("/task_status_update/<int:id>", methods=['GET', 'POST'])
@login_required
def task_status_update(id):
    form = TaskStatusUpdateForm()
    done_task = models.Tasks.query.get(id)

    if form.validate_on_submit():
        done_task.status = form.status.data
        db.session.commit()
        return redirect(url_for('records'))

    return render_template("task_status_update.html", form=form, done_task=done_task)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestUpdateForm()
    if form.validate_on_submit():
        user = Customers.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('The email with all instructions how to reset password was sent to you.', 'info')
        return redirect(url_for('register'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Customers.verify_reset_token(token)
    if user is None:
        flash('Request rejected ', 'warning')
        return redirect(url_for('reset_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password is updated. You can login now', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profilio_nuotraukos', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.photo.data:
            photo = save_picture(form.photo.data)
            current_user.photo = photo
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account is updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    photo = url_for('static', filename='profilio_nuotraukos/' + current_user.photo)
    return render_template('account.html', title='Account', form=form, photo=photo)
