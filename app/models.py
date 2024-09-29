from .extensions import db

from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    student = db.relationship(
        "Student",
        backref=db.backref("user", lazy=True),
        single_parent=True,
        uselist=False,
    )

    admin = db.relationship(
        "Admin",
        backref=db.backref("user", lazy=True),
        single_parent=True,
        uselist=False,
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    students = db.relationship('Student', back_populates='course')


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique= False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user = db.relationship('User', backref='student')
    course_id = db.Column(db.ForeignKey('course.id'))

    course = db.relationship('Course', back_populates='students')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='admin')  # Add email for admin
    # course_id = db.Column(db.ForeignKey('course.id'))
    
    # course = db.relationship('Course', back_populates='admins')

class Scholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    criteria = db.Column(db.String(255), nullable=False)

class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)












# # Adding multiple courses to the database session




# # Commit the session to save changes to the database
# db.session.commit()
