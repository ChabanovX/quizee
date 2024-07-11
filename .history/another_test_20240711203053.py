import unittest
from flask_testing import TestCase
from config import db, app
from models import User, Quiz


class UserTests(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'test_secret'
        return app

    def setUp(self):
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register(self):
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "password"
        }
        response = self.client.post("/register", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["message"], "User created.")

    def test_login(self):
        user = User(email="test@example.com", username="testuser", password="password")
        db.session.add(user)
        db.session.commit()

        data = {
            "email": "test@example.com",
            "password": "password"
        }
        response = self.client.post("/login", json=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)

    def test_create_quiz(self):
        user = User(email="test@example.com", username="testuser", password="password")
        db.session.add(user)
        db.session.commit()

        data = {
            "naming": "Test Quiz",
            "questions": [
                {
                    "text": "What is the capital of France?",
                    "answers": [
                        {
                            "text": "Paris",
                            "is_correct": True
                        },
                        {
                            "text": "London",
                            "is_correct": False
                        }
                    ],
                    "has_multiple_right_answers": False
                }
            ]
        }
        response = self.client.post("/create_quiz", ()}"}, json=data)
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["message"], "Quiz created.")


if __name__ == "__main__":
    unittest.main()