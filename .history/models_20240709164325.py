from config import db
from datetime import datetime, UTC

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

class Question(db.Model):
    # Question has a text and answers. Some answers are correct and some are wrong
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

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naming = db.Column(db.String(80), nullable=False, unique=True)
    questions = db.relationship("Question", backref="quiz")
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"))

    def __repr__(self) -> str:
        return f"<Quiz: {self.naming}>"

    def to_json(self):
        return {
            "id": self.id,
            "naming": self.naming,
            "questions": [question.to_json() for question in self.questions]
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)  # hash of password
    creation_date = db.Column(db.DateTime, default=datetime.now(UTC))
    
    # TODO Statistics
    
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
