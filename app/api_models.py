from .extensions import api
from flask_restx import fields


student_model = api.model("Student", {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    # "course": fields.Nested(course_model)
})

course_model = api.model("Course", {
    "id": fields.Integer,
    "name": fields.String,
    "students": fields.List(fields.Nested(student_model))
})

# student_model = api.model("Student", {
#     "id": fields.Integer,
#     "name": fields.String,
#     # "course": fields.Nested(course_model)
# })

course_input_model = api.model("CourseInput", {
    "name": fields.String,
})

student_input_model = api.model("StudentInput", {
    "name": fields.String,
    "course_id": fields.Integer
})

event_model = api.model("Event", {
    "id": fields.Integer,
    "name": fields.String,
    "date": fields.DateTime,
    "description": fields.String
})

event_input_model = api.model("EventInput", {
    "name": fields.String,
    "date": fields.DateTime,
    "description": fields.String
})


# Scholarship Model
scholarship_model = api.model("Scholarship", {
    "id": fields.Integer,
    "name": fields.String,
    "amount": fields.Float,
    "criteria": fields.String
})

# Scholarship Input Model
scholarship_input_model = api.model("ScholarshipInput", {
    "name": fields.String(required=True, description="Scholarship name"),
    "amount": fields.Float(required=True, description="Scholarship amount"),
    "criteria": fields.String(required=True, description="Eligibility criteria")
})

# FAQ Model
faq_model = api.model("FAQ", {
    "id": fields.Integer,
    "question": fields.String,
    "answer": fields.String
})

# FAQ Input Model
faq_input_model = api.model("FAQInput", {
    "question": fields.String(required=True, description="FAQ question"),
    "answer": fields.String(required=True, description="FAQ answer")
})

# Contact Message Model
contact_message_model = api.model("ContactMessage", {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "message": fields.String
})

# Contact Message Input Model
contact_message_input_model = api.model("ContactMessageInput", {
    "name": fields.String(required=True, description="Sender's name"),
    "email": fields.String(required=True, description="Sender's email"),
    "message": fields.String(required=True, description="Message content")
})

login_post = api.model(
    "login",
    {
        "username": fields.String(
            required=True, description="The username", example="admin"
        ),
        "password": fields.String(
            required=True, description="The password", example="admin"
        ),
    },
)

registration_model = api.model("Registration", {
    "username": fields.String(required=True, description="The username"),
    "password": fields.String(required=True, description="The password"),
    # "admin": fields.Boolean(required=False, description="Is the user an admin"),
    "student": fields.Boolean(required=False, description="Is the user a student"),
})
