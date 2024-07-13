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
    title='Quizee API',
    version='1.0',
    description='API for Quizee WebApp',
    authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Type in the '*Value*' input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
        }
    }
)

CORS(app)
