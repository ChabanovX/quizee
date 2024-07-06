from flask import request, jsonify
from config import app, db
from models import User, Topic, Quiz, Question, Answer

import models
import json


@app.route("/")
def main_page():
    return "<h1>Welcome to the Quizee backend!</h1>"


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
    
    instance = models.instances[instance_name].query.get(id)

    if not instance:
        return jsonify({"message": f"{instance_name}_{id} not found."}), 404
    
    return jsonify(instance.to_json())


@app.route("/<instance_name>/<int:id>", methods=["DELETE"])
def delete_instance_by_id(instance_name, id):
    if instance_name not in models.instances:
        return jsonify({"message": "{} is not a valid instance.".format(instance_name)}), 400
    
    instance = models.instances[instance_name].query.get(id)
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
    has_multiple_answers = request.json.get("hasMultipleAnswers")

    if not text or not answers or not has_multiple_answers:
        return jsonify({"message": "You must inclide all the info."}), 400,

    # Answer should follow JSON format of an answer.
    answers = [Answer(text=x["text"], is_correct=x["is_correct"]) for x in json.loads(answers)]
    new_question = Question(text=text, answers=answers, )

    try:
        db.session.add(new_question)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
    
    return jsonify({"message": "Question created."}), 201


@app.route("/update_question/<int:question_id>", methods=["POST"])
def update_question(question_id):
    question = Question.query.get(question_id)

    if not question:
        return jsonify({"message": "Question not found."}), 404
    
    data = request.json
    question.text = data.get("text", question.text)
    question.answers = data.get("answers", question.answers)

    try:
        db.session.commit()
    except Exception as e:
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

        for answer in json.loads(question)["answers"]:
            answer_dict = json.loads(answer)
            answer_instances.append(Answer(text=answer_dict["text"], is_correct=answer_dict["is_correct"]))

        question_dict = json.loads(question)
        question_instances.append(Question(text=question_dict["text"], answers=answer_instances))

    new_quiz = Quiz(naming=naming, questions=question_instances)
    try:
        db.session.add(new_quiz)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Quiz created."}), 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
    