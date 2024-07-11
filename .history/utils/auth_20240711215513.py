from config import db, login_manager
from models import User

from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_required
def logout() -> None:
    logout_user()


def register(email: str, username: str, password: str, **kwargs) -> None:
    if User.query.filter_by(email=email).first() is not None:
        raise Exception("User with this email already exists")
    
    if User.query.filter_by(username=username).first() is not None:
        raise Exception("User with this username already exists")
    
    try:
        user = User(email=email, username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e


def login(username: str, password: str, **kwargs) -> str:
    user = User.query.filter_by(username=username).first()
    if user is None or not check_password_hash(user.password, password):
        raise Exception("Invalid credentials.")
    
    login_user(user)
    print(current_user)
    
