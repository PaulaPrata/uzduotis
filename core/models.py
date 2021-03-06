from core import db, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

association_table = db.Table('association', db.metadata,
      db.Column('customers_id', db.Integer, db.ForeignKey('customers.id')),
      db.Column('tasks_id', db.Integer, db.ForeignKey('tasks.id')))


class Customers(db.Model, UserMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column("password", db.String(60), unique=True, nullable=False)
    photo = db.Column(db.String(20), nullable=False, default='default.jpg')
    tasks = db.relationship("Tasks", secondary= association_table,back_populates="customers")


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Customers.query.get(user_id)

class Tasks (db.Model):
    __tablename__='tasks'
    customer_id= db.Column(db.Integer)
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String(80))
    status = db.Column(db.String(80))
    project_id = db.Column(db.Integer,db.ForeignKey("projects.id"))
    customers=db.relationship("Customers", secondary= association_table,back_populates="tasks")
    task_name = db.Column(db.String(80))


class Projects (db.Model):
    __tablename__='projects'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(80))
    customer_id= db.Column(db.Integer, db.ForeignKey("customers.id"))
    tasks = db.relationship("Tasks", lazy=True)