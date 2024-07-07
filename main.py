from flask import request, jsonify
from config import app, db, jwt
from models import User, Topic, Quiz, Question, Answer # should not be there TODO:

from flask_jwt_extended import jwt_required, get_jwt_identity # needed for protected routes

import models
import utils.auth
import utils.utils

import json


@app.route("/")
def main_page():
    return "<h1>Welcome to the Quizee backend!</h1>"


@app.route("/register", methods=["POST"])
def register():
    try:
        utils.auth.register(**request.get_json())

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
    return jsonify({"message": "User created."}), 201


@app.route("/login", methods=["POST"])
def login():
    try:
        token = utils.auth.login(**request.get_json())

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    return jsonify({"message": "Login successful.", "access_token": token})


@app.route("/<instance_name>", methods=["GET"])
def get_all_instances(instance_name):
    if instance_name not in models.instances:
        return jsonify({"message": "{} is not a valid instance.".format(instance_name)}), 400
    else:
        return jsonify({instance_name: [x.to_json() for x in models.instances[instance_name].query.all()]})


@app.route("/<instance_name>/<int:id>")
def get_instance_by_id(instance_name, id):
    if instance_name not in models.instances:
        return jsonify({"message": "{} is not a valid instance.".format(instance_name)}), 400
    
    # instance = models.instances[instance_name].query.get(id) Legacy
    instance = db.session.get(models.instances[instance_name], id)

    if not instance:
        return jsonify({"message": f"{instance_name}_{id} not found."}), 404
    
    return jsonify(instance.to_json())


@app.route("/<instance_name>/<int:id>", methods=["DELETE"])
def delete_instance_by_id(instance_name, id):
    if instance_name not in models.instances:
        return jsonify({"message": "{} is not a valid instance.".format(instance_name)}), 400
    
    instance = db.session.get(models.instances[instance_name], id)
    if not instance:
        return jsonify({"message": "Instance not found."}), 404
    
    try:
        db.session.delete(instance)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": f"{instance_name}_{id} deleted."}), 200


@app.route("/create_question", methods=["POST"])
def create_question():
    text = request.json.get("text")
    answers = request.json.get("answers")
    has_multiple_right_answers = request.json.get("hasMultipleRightAnswers")

    if not text or not answers or not has_multiple_right_answers:
        return jsonify({"message": "You must inclide all the info."}), 400,

    # Answer should follow JSON format of an answer.
    answers = [Answer(text=x["text"], is_correct=x["is_correct"]) for x in json.loads(answers)]
    new_question = Question(text=text, answers=answers, has_multiple_right_answers=has_multiple_right_answers)

    try:
        db.session.add(new_question)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
    
    return jsonify({"message": "Question created."}), 201


@app.route("/update_question/<int:question_id>", methods=["POST"])
def update_question(question_id):
    question = db.session.get(Question, question_id)

    if not question:
        return jsonify({"message": "Question not found."}), 404
    
    data = request.json
    question.text = data.get("text", question.text)
    question.answers = data.get("answers", question.answers)
    question.has_multiple_right_answers = data.get("hasMultipleRightAnswers", question.has_multiple_right_answers)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Question updated."}), 200


@app.route("/create_quiz", methods=["POST"])
def create_quiz():
    naming = request.json.get("naming")
    questions = request.json.get("questions")

    if not naming or not questions:
        return jsonify({"message": "You must inclide naming and questions"}), 400,

    # Now we should create real instances of questions and answers.
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
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Quiz created."}), 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
    