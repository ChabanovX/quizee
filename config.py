from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret-lol"

db = SQLAlchemy(app)
jwt = JWTManager(app)
api = Api(app, 
    doc="/swagger",
    title='Quiz API',
    version='1.0',
    description='A simple Quiz API',
    authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
        }
    }
)

CORS(app)
