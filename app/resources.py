from flask_restx import Namespace, Resource
from app.models import Course
from .models import Student, User
from .api_models import student_model
from .api_models import course_model
from .api_models import course_input_model
from .api_models import student_input_model
from .models import Event
from .api_models import event_model
from .api_models import event_input_model
from .models import Scholarship, FAQ, ContactMessage
from .api_models import scholarship_model
from .api_models import scholarship_input_model
from .api_models import faq_model
from .api_models import faq_input_model
from .api_models import contact_message_model
from .api_models import contact_message_input_model
from .api_models import registration_model
from .api_models import login_post
from .extensions import db
from flask import request

ns = Namespace("api")

@ns.route("/hello")
class Hello(Resource):
    def get(self):
        return {'hello': 'world'}
    

@ns.route("/courses")
class CoursesListAPI(Resource):
    @ns.marshal_list_with(course_model)
    def get(self):
        return Course.query.all()
    
    @ns.expect(course_input_model)
    @ns.marshal_with(course_model, code=201)
    def post(self):
        print(ns.payload)
        course = Course(name=ns.payload["name"])
        db.session.add(course)
        db.session.commit()
        return course, 201
    
@ns.route("/course/<int:id>")
class CourseAPI(Resource):
    @ns.marshal_with(course_model)
    def get(self, id):
        return Course.query.get(id)
    
    def delete(self, id):
        course = Course.query.get(id)
        db.session.delete(course)
        db.session.commit()
        return None, 204
    
    @ns.expect(course_input_model)
    @ns.marshal_with(course_model)
    def put(self, id):
        course = Course.query.get(id)
        course.name = ns.payload["name"]
        db.session.commit()
        return course
    
@ns.route("/student")
class StudentAPI(Resource):
    @ns.marshal_list_with(student_model)
    def get(self):
        return Student.query.all()
    
    @ns.expect(student_input_model)
    @ns.marshal_with(student_model, code=201)
    def post(self):
        print(ns.payload)
        student = Student(name=ns.payload["name"], course_id = ns.payload["course_id"])
        db.session.add(student)
        db.session.commit()
        return student, 201
    
@ns.route("/student/<int:id>")
class StudentAPI(Resource):
    @ns.marshal_with(student_model)
    def get(self, id):
        return Student.query.get(id)
    
    def delete(self, id):
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()
        return None, 204
    
    @ns.expect(student_input_model)
    @ns.marshal_with(student_model)
    def put(self, id):
        student = Student.query.get(id)
        student.name = ns.payload["name"]
        student.course_id = ns.payload["course_id"]
        db.session.commit()
        return student
    

# 1. Create a new model called Event with the following fields: id, name, date, description

@ns.route("/events")
class EventsListAPI(Resource):
    @ns.marshal_list_with(event_model)
    def get(self):
        return Event.query.all()
    
    @ns.expect(event_input_model)
    @ns.marshal_with(event_model, code=201)
    def post(self):
        print(ns.payload)
        event = Event(name=ns.payload["name"], date=ns.payload["date"], description=ns.payload["description"])
        db.session.add(event)
        db.session.commit()
        return event, 201
    


@ns.route("/scholarships")
class ScholarshipsListAPI(Resource):
    @ns.marshal_list_with(scholarship_model)
    def get(self):
        return Scholarship.query.all()
    
    @ns.expect(scholarship_input_model)
    @ns.marshal_with(scholarship_model, code=201)
    def post(self):
        print(ns.payload)
        scholarship = Scholarship(name=ns.payload["name"], amount=ns.payload["amount"], criteria=ns.payload["criteria"])
        db.session.add(scholarship)
        db.session.commit()
        return scholarship, 201

@ns.route("/faqs")
class FAQsListAPI(Resource):
    @ns.marshal_list_with(faq_model)
    def get(self):
        return FAQ.query.all()
    
    @ns.expect(faq_input_model)
    @ns.marshal_with(faq_model, code=201)
    def post(self):
        print(ns.payload)
        faq = FAQ(question=ns.payload["question"], answer=ns.payload["answer"])
        db.session.add(faq)
        db.session.commit()
        return faq, 201

@ns.route("/contact")
class ContactMessagesListAPI(Resource):
    @ns.marshal_list_with(contact_message_model)
    def get(self):
        return ContactMessage.query.all()
    
    @ns.expect(contact_message_input_model)
    @ns.marshal_with(contact_message_model, code=201)
    def post(self):
        print(ns.payload)
        contact_message = ContactMessage(name=ns.payload["name"], email=ns.payload["email"], message=ns.payload["message"])
        db.session.add(contact_message)
        db.session.commit()
        return contact_message, 201


    # login, logout, registration, event, scholarship, course, student, admin, user, contact us, faq, about us, home
    #  we need these api endpoints, I have already created student and course, can you do the rest?


#login

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)


@ns.route("/login")
class LoginAPI(Resource):
    @ns.expect(login_post)
    @ns.doc(description="This is the login endpoint")
    def post(self):
        username = ns.payload.get("username")
        password = ns.payload.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            access_token = create_access_token(identity=user.id)
            return {
                "access_token": access_token,
                "admin": bool(user.admin),
                "student": bool(user.student),
                }
        else:
            return {"message": "Invalid credentials"}, 401

@ns.route("/register")
class RegistrationAPI(Resource):
    @ns.expect(registration_model)
    @ns.doc(description="This is the registration endpoint")
    def post(self):
        username = request.json.get("username")
        password = request.json.get("password")
        # instructor = request.json.get("instructor", False)
        student = request.json.get("student", False)

        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {"message": "User already exists."}, 400

        # Create a new user instance
        new_user = User(username=username, student=student)

        # Hash the password and save the user to the database
        new_user.set_password(password)  # Assuming you have a method to hash the password
        db.session.add(new_user)
        db.session.commit()

        # Generate an access token
        access_token = create_access_token(identity=new_user.id)

        return {
            "message": "User registered successfully.",
            "access_token": access_token,
            "instructor": bool(new_user.instructor),
            "student": bool(new_user.student),
        }, 201
