from flask import render_template, redirect, flash,url_for, request
from core import app, db, models, Bcrypt, login_manager
from flask_login import current_user, login_user, logout_user, login_required
from core.models import Customers
from core import app
from core.forms import RegForm, LoginForm, RecordForm, TaskForm
from datetime import datetime

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
            login_user(user,remember=form.remember_me.data)
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
        new_task= models.Tasks(task_name=form.task_name.data, customer_id=current_user.id, project_id=form.project.data.id )
        db.session.add(new_task)
        db.session.commit()
        flash(f"New Task is added to Project", 'success')
        return redirect(url_for('records'))
    return render_template("add_task.html", form=form)


# @app.route("/atsijungti")
# def atsijungti():
#     logout_user()
#     return redirect(url_for('index'))
#
# @app.route("/nauja_uzduotis", methods=["GET", "POST"])
# def saskaita_new():
#     db.create_all()
#     forma = SaskaitaForm()
#     if forma.validate_on_submit():
#         nauja_saskaita = models.Saskaita(numeris=forma.numeris.data, zmogus_id=forma.zmogus.data.id, bankas_id=forma.bankas.data.id, balansas=forma.balansas.data)
#         db.session.add(nauja_saskaita)
#         db.session.commit()
#         return redirect(url_for('accounts'))
#     return render_template("prideti_saskaita.html", form=forma)
#
# # @app.route("/saskaita_update/<int:id>", methods=['GET', 'POST'])
# # def saskaita_update(id):
# #     form = SaskaitaForm()
# #     saskaita = models.Saskaita.query.get(id)
# #     if form.validate_on_submit():
# #         saskaita.numeris = form.numeris.data
# #         saskaita.zmogus_id = form.zmogus.data.id
# #         saskaita.bankas_id = form.bankas.data.id
# #         saskaita.balansas = form.balansas.data
# #         db.session.commit()
# #         return redirect(url_for('accounts'))
#     return render_template("saskaita_update.html", form=form, saskaita=saskaita)