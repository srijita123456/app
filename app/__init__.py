from flask import Flask

from .extensions import db, api, jwt
from .resources import ns

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

# Initialize JWTManager
    jwt.init_app(app)

    api.init_app(app)
    db.init_app(app)

    api.add_namespace(ns)

    return app

