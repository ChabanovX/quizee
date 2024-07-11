from models import Quiz, Question, Answer
from config import db

from flask_login import current_user, login_required


def get_quizzes() -> list:
    quizzes = Quiz.query.filter_by(user_id=current_user.id).all()
    return [quiz.to_json() for quiz in quizzes]


def create_quiz(naming: str, questions: list) -> None:
    question_instances = []
    for question in questions:
        answer_instances = []

        for answer in question["answers"]:
            answer_instances.append(Answer(text=answer["text"], is_correct=answer["is_correct"]))

        question_instances.append(Question(text=question["text"], answers=answer_instances,
                                            has_multiple_right_answers=question["hasMultipleRightAnswers"]))

    new_quiz = Quiz(naming=naming, questions=question_instances)
    try:
        db.session.add(new_quiz)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
