from models import Quiz, Question, Answer
from config import db

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
