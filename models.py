from datetime import datetime, UTC
from flask_restx import fields

from config import db, api


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=True)

    def __repr__(self) -> str:
        return f"<Answer: {self.text}. Is correct: {self.is_correct}>"

    def to_json(self):
        return {
            "id": self.id,
            "text": self.text,
            "is_correct": self.is_correct
        }
    
    @staticmethod
    def to_api_model():
        return api.model('Answer', {
            'text': fields.String(required=True, description='Answer text'),
            'is_correct': fields.Boolean(required=True, description='Is the answer correct')
        })


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(800), nullable=False)
    answers = db.relationship("Answer", backref="question")
    has_multiple_right_answers = db.Column(db.Boolean, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=True)

    def __repr__(self) -> str:
        return f"<Question: {self.text}>"

    def to_json(self):
        return {
            "id": self.id,
            "text": self.text,
            "answers": [answer.to_json() for answer in self.answers],
            "hasMultipleRightAnswers": self.has_multiple_right_answers
        }
    
    @staticmethod
    def to_api_model():
        return api.model('Question', {
            'text': fields.String(required=True, description='Question text'),
            'answers': fields.List(fields.Nested(Answer.to_api_model()), required=True, description='List of answers'),
            'hasMultipleRightAnswers': fields.Boolean(required=True, description='Does the question have multiple correct answers')
        })


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naming = db.Column(db.String(80), nullable=False, unique=False)
    questions = db.relationship("Question", backref="quiz")
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"<Quiz: {self.naming}>"

    def to_json(self):
        return {
            "id": self.id,
            "naming": self.naming,
            "questions": [question.to_json() for question in self.questions]
        }
    
    @staticmethod
    def to_api_model():
        return api.model('Quiz', {
            'naming': fields.String(required=True, description='Quiz name'),
            'questions': fields.List(fields.Nested(Question.to_api_model()), required=True, description='List of questions')
        })


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.now(UTC))
    quizzes = db.relationship("Quiz", backref="user")
    
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
    
    @staticmethod
    def to_api_model_register():
        return api.model('User Register', {
            'email': fields.String(required=True),
            'username': fields.String(required=True),
            'password': fields.String(required=True)
        })
    
    @staticmethod
    def to_api_model_login():
        return api.model('User Login', {
            'username': fields.String(required=True),
            'password': fields.String(required=True)
        })


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naming = db.Column(db.String(80), nullable=False, unique=True)
    quizzes = db.relationship("Quiz", backref="topic")

    def __repr__(self) -> str:
        return f"<Topic: {self.naming}>"

    def to_json(self):
        return {
            "id": self.id,
            "naming": self.naming
        }
