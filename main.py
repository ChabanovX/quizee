from flask import request, jsonify
from config import app, db
from models import User, Topic, Quiz, Question, Answer


@app.route("/")
def main_page():
    return "<h1>Welcome to the Quizee backend!</h1>"


@app.route("/create_answer", methods=["POST"])
def create_answer():
    text = request.json.get("text")
    is_correct = request.json.get("is_correct")

    if not text or not is_correct:
        return jsonify({"message": "You must inclide text and is_correct."}), 400,

    new_answer = Answer(text=text, is_correct=is_correct)
    try:
        db.session.add(new_answer)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Answer created."}), 201


@app.route("/create_question", methods=["POST"])
def create_question():
    text = request.json.get("text")
    answers = request.json.get("answers")

    if not text or not answers:
        return jsonify({"message": "You must inclide text and answers."}), 400,

    new_question = Question(text=text, answers=answers)
    try:
        db.session.add(new_question)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Question created."}), 201
    

@app.route("/quizzes", methods=["GET"])
def get_quizzes():
    quizzes = Quiz.query.all()
    json_quizzes = list(map(lambda x: x.to_json(), quizzes))

    return jsonify({"topics": json_quizzes}), 200


@app.route("/create_quiz", methods=["POST"])
def create_quiz():
    # Quiz has questions. Each question has answers. Some questions are multiple choice.
    naming = request.json.get("naming")

    if not naming:
        return jsonify({"message": "You must inclide naming."}), 400,

    new_quiz = Quiz(naming=naming)
    try:
        db.session.add(new_quiz)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Quiz created."}), 201


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    json_users = list(map(lambda x: x.to_json(), users))

    return jsonify({"users": json_users}), 200


@app.route("/create_user", methods=["POST"])
def create_user():
    email = request.json.get("email")
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not email:
        return jsonify({"message": "You must inclide username and email."}), 400,

    new_user = User(username=username, password=password, email=email)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "User created."}), 201


@app.route("/topics", methods=["GET"])
def get_topics():
    topics = Topic.query.all()
    json_topics = list(map(lambda x: x.to_json(), topics))

    return jsonify({"topics": json_topics}), 200


@app.route("/create_topic", methods=["POST"])
def create_topic():
    naming = request.json.get("naming")

    if not naming:
        return jsonify({"message": "You must inclide naming."}), 400,

    new_topic = Topic(naming=naming)
    try:
        db.session.add(new_topic)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Topic created."}), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # some_topic = Topic(naming="Narcotics")
        # quiz1 = Quiz(naming="Woman with a headache", topic=some_topic)
        # print(quiz1.topic)
        # db.session.add_all([some_topic, quiz1])
        # db.session.commit()

    app.run(debug=True)
