from models import Quiz, Question, Answer
from config import db

from flask_login import current_user, login_required


@login_required
def get_quizzes() -> list:
    quizzes = Quiz.query.filter_by(user_id=current_user.id).all()
    return [quiz.to_json() for quiz in quizzes]


@login_required
def create_quiz(naming: str, questions: list) -> None:
    question_instances = []
    for question in questions:
        answer_instances = []

        for answer in question["answers"]:
            answer_instances.append(Answer( text=answer["text"], 
                                            is_correct=answer["is_correct"],
                                            question_id=question["id"]))

        question_instances.append(Question( text=question["text"],
                                            answers=answer_instances,
                                            has_multiple_right_answers=question["hasMultipleRightAnswers"],
                                            quiz_id=None))

    new_quiz = Quiz(naming=naming, questions=question_instances, user_id=current_user.id)

    # We still need to  quiz_id in questions
    for question in new_quiz.questions:
        question.quiz_id = new_quiz.id

    try:
        db.session.add(new_quiz)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
