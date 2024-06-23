from config import db
from datetime import datetime, UTC
# User
# Topic -> Quiz
# Quiz

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naming = db.Column(db.String(80), nullable=False, unique=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable=True)

    def __repr__(self) -> str:
        return f"<Quiz: {self.naming}>"

    def to_json(self):
        return {
            "id": self.id,
            "naming": self.naming
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)  # hash of password
    creation_date = db.Column(db.Date, default=datetime.now(UTC))
    # Statistics
    
    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "creationDate": self.creation_date
        }
    
    def __repr__(self) -> str:
        return f"<User: {self.username} with email: {self.email}>"


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naming = db.Column(db.String(80), nullable=False, unique=True)
    quizzes = db.relationship("Quiz", backref="topic")

    def to_json(self):
        return {
            "id": self.id,
            "naming": self.naming
        }
