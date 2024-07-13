from config import db
from models import User

from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError


def register(email: str, username: str, password: str, **kwargs) -> None:
    if User.query.filter_by(email=email).first() is not None:
        raise Exception("User with this email already exists")
    
    if User.query.filter_by(username=username).first() is not None:
        raise Exception("User with this username already exists")
    
    try:
        user = User(email=email, username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Database integrity error")
    except Exception as e:
        db.session.rollback()
        raise Exception(f"An error occurred: {e}")


def login(username: str, password: str, **kwargs) -> str:
    user = User.query.filter_by(username=username).first()
    if user is None or not check_password_hash(user.password, password):
        raise Exception("Invalid credentials.")
    
    access_token = create_access_token(identity=user.id)
    return access_token
    
