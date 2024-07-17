from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm.exc import UnmappedInstanceError

from models import User, Quiz, Question, Answer
from config import db


@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if user:
        return user.to_json()
    raise Exception("User not found")


@jwt_required()
def get_quizzes() -> list:
    current_user = get_jwt_identity()
    try:
        quizzes = Quiz.query.filter_by(user_id=current_user).all()
        return [quiz.to_json() for quiz in quizzes]
    except Exception as e:
        raise Exception(f"An error occurred while getting quizzes: {e}")


@jwt_required()
def create_quiz(quizTitle: str, questions: list) -> None:
    current_user = get_jwt_identity()
    question_instances = []

    for question in questions:
        answer_instances = [
            Answer(answer_text=answer["answerText"], is_correct=answer["isCorrect"])
            for answer in question["answers"]
        ]

        question_instances.append(
            Question(
                question_text=question["questionText"],
                answers=answer_instances,
                has_multiple_right_answers=question["hasMultipleRightAnswers"],
                quiz_id=None
            )
        )

    new_quiz = Quiz(quiz_title=quizTitle, questions=question_instances, user_id=current_user)

    # We still need to set quiz_id in questions (MAYBE)
    for question in new_quiz.questions:
        question.quiz_id = new_quiz.id

    try:
        db.session.add(new_quiz)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"An error occurred while creating quiz: {e}")
    
@jwt_required()
def delete_quiz(quiz_id: int) -> None:
    current_user = get_jwt_identity()
    try:
        quiz = Quiz.query.filter_by(id=quiz_id, user_id=current_user).first()
        db.session.delete(quiz)
        db.session.commit()
    except UnmappedInstanceError:
        db.session.rollback()
        raise Exception("Quiz with this id was not found.")
    except Exception as e:
        db.session.rollback()
        raise e 
