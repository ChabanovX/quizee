from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = "super secret key"
login_manager = LoginManager()
login_manager.init_app(app)


db = SQLAlchemy(app)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


