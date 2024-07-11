from flask import request, jsonify
from config import app, db

import models
import utils.auth
import utils.utils


@app.route("/")
def main_page():
    return "<h1>Welcome to the Quizee backend!</h1>"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            utils.auth.register(**request.get_json())
        except Exception as e:
            return jsonify({"message": str(e)}), 500
        
        return jsonify({"message": "User created."}), 201
    
    return "<h1>Welcome to the Register Page!</h1>"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            utils.auth.login(**request.get_json())
        except Exception as e:
            return jsonify({"message": str(e)}), 401

        return jsonify({"message": "Login successful."}), 200

    return "<h1>Welcome to the Login Page!</h1>"


# Login required
@app.route("/logout", methods=["GET"])
def logout():
    utils.auth.logout()
    return jsonify({"message": "Logout successful."}), 200


# Login required
@app.route("/quizzes", methods=["GET"])
def get_quizzes():
    return jsonify(utils.utils.get_quizzes()), 200


# Login required
@app.route("/create_quiz", methods=["GET", "POST"])
def create_quiz():
    try:
        utils.utils.create_quiz(**request.get_json())
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Quiz created."}), 201




# @app.route("/<instance_name>", methods=["GET"])
# def get_all_instances(instance_name):
#     if not getattr(models, instance_name, False):
#         return jsonify({"message": "{} is not a valid instance.".format(instance_name)}), 400
#     else:
#         return jsonify({instance_name: [x.to_json() for x in getattr(models, instance_name).query.all()]})


# @app.route("/<instance_name>/<int:id>")
# def get_instance_by_id(instance_name, id):
#     if not getattr(models, instance_name, False):
#         return jsonify({"message": "{} is not a valid instance.".format(instance_name)}), 400
    
#     instance = db.session.get(getattr(models, instance_name), id)
#     if not instance:
#         return jsonify({"message": f"{instance_name}_{id} not found."}), 404
    
#     return jsonify(instance.to_json())


# @app.route("/<instance_name>/<int:id>", methods=["DELETE"])
# def delete_instance_by_id(instance_name, id):
#     if not getattr(models, instance_name, False):
#         return jsonify({"message": "{} is not a valid instance.".format(instance_name)}), 400
    
#     instance = db.session.get(getattr(models, instance_name), id)
#     if not instance:
#         return jsonify({"message": "Instance not found."}), 404
    
#     try:
#         db.session.delete(instance)
#         db.session.commit()
#     except Exception as e:
#         return jsonify({"message": str(e)}), 400
    
#     return jsonify({"message": f"{instance_name}_{id} deleted."}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
    