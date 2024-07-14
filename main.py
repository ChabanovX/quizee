from flask import request, jsonify, make_response
from flask_restx import Resource

from config import app, api, db
import utils.utils
import utils.auth
import models


# API namespaces
auth_ns = api.namespace("auth", description="Authentication related operations")
quiz_ns = api.namespace("quiz", description="Quiz related operations")
general_ns = api.namespace("general", description="General operations")


@general_ns.route("/")
class MainPage(Resource):
    def get(self):
        return "<h1>Welcome to the Quizee backend!</h1>", 200
    

@general_ns.route("/profile")
class Profile(Resource):
    @api.doc(security='Bearer Auth')
    def get(self):
        try:
            profile_data = utils.utils.profile()
            return make_response(jsonify({"profile": profile_data}), 200)
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 404)


@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(models.User.to_api_model_register())
    def post(self):
        try:
            utils.auth.register(**request.get_json())
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)
        
        return make_response(jsonify({"message": "User created."}), 201)


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(models.User.to_api_model_login())
    def post(self):
        try:
            token = utils.auth.login(**request.get_json())
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 401)

        return make_response(jsonify(access_token=token), 200)


@quiz_ns.route("/quizzes")
class Quizzes(Resource):
    @api.doc(security='Bearer Auth')
    def get(self):
        return make_response(utils.utils.get_quizzes(), 200)


@quiz_ns.route("/create-quiz")
class CreateQuiz(Resource):
    @quiz_ns.expect(models.Quiz.to_api_model())
    @api.doc(security='Bearer Auth')
    def post(self):
        try:
            utils.utils.create_quiz(**request.get_json())
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 400)
        
        return make_response(jsonify({"message": "Quiz created."}), 201)


@quiz_ns.route("/delete-quiz/<int:quiz_id>")
class DeleteQuiz(Resource):
    @api.doc(security='Bearer Auth')
    def delete(self, quiz_id):
        try:
            utils.utils.delete_quiz(quiz_id)
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 400)
        
        return make_response(jsonify({"message": "Quiz deleted."}), 200)
    

# Not safe. Should be used only for testing
@general_ns.route("/<instance_name>")
class GetAllInstances(Resource):
    def get(self, instance_name):
        if not getattr(models, instance_name, False):
            return make_response(jsonify({"message": "{} is not a valid instance.".format(instance_name)}), 400)
        else:
            return make_response(jsonify({instance_name: [x.to_json() for x in getattr(models, instance_name).query.all()]}), 200)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
    