import unittest
import requests
from models import User, db
from config import app

class TestQuizeeBackend(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://127.0.0.1:5000"

    def test_main_page(self):
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)

    # def test_get_user(self):
    #     for i in range(1, 3 + 1):
    #         response = requests.get(self.base_url + "/User/" + str(i))
    #         print(response.content)

    # def test_register(self):
    #     json_data = {
    #         "username": "admin",
    #         "email": "admin@qa.com",
    #         "password": "ebaloff"
    #     }

    #     response = requests.post(self.base_url + "/register", json=json_data)
    #     print(response.content)
    #     self.assertEqual(response.status_code, 201)

    def test_login_and_creating(self):
        json_data_reg = {
            "email": "adminhuyhuy@qa.com",
            "username": "shithuy",
            "password": "password"
        }
        json_data = {
            "username": "shithuy",
            "password": "password"
        }
        with requests.Session() as session:
            response = session.post(self.base_url + "/register", json=json_data_reg)
            print(response.content)
            response = session.post(self.base_url + "/login", json=json_data)
            print(response.content)

            response = session.post(self.base_url + "/create_quiz", json={
            "naming": "Quiz 1234",
            "questions": [{
                "text": "Question 1",
                "hasMultipleRightAnswers": False,
                "answers": [{
                    "text": "Answer 1",
                    "is_correct": True
                }, {
                    "text": "Answer 2",
                    "is_correct": False
                }]
            }, 
            {
                "text": "Question 2",
                "hasMultipleRightAnswers": False,
                "answers": [{
                    "text": "Answer 1",
                    "is_correct": True
                }, {
                    "text": "Answer 2",
                    "is_correct": False
                }]
            }]
        })
            print(response.content)
            response = session.get(self.base_url + "/Quiz")
            print(response.content)
            # self.assertEqual(response.status_code, 201)


    # def test_get_user(self):
    #     for i in range(1, 10):
    #         response = requests.get(self.base_url + "/User/" + str(i))
    #         print(response.content)
            # self.assertEqual(response.status_code, 200)


    # def test_create_quiz(self):
    #     response = requests.post(self.base_url + "/create_quiz", json={
    #         "naming": "Quiz 1234",
    #         "questions": [{
    #             "text": "Question 1",
    #             "hasMultipleRightAnswers": False,
    #             "answers": [{
    #                 "text": "Answer 1",
    #                 "is_correct": True
    #             }, {
    #                 "text": "Answer 2",
    #                 "is_correct": False
    #             }]
    #         }, 
    #         {
    #             "text": "Question 2",
    #             "hasMultipleRightAnswers": False,
    #             "answers": [{
    #                 "text": "Answer 1",
    #                 "is_correct": True
    #             }, {
    #                 "text": "Answer 2",
    #                 "is_correct": False
    #             }]
    #         }]
    #     })
    #     print(response.content)
    #     self.assertEqual(response.status_code, 201)
    
    # def test_delete_user(self):
    #     for i in range(1, 10):
    #         response = requests.delete(self.base_url + "/User/" + str(i))
    #         print(json.loads(response.content))

    # def test_get_quizzes(self):
    #     for i in range(1, 3 + 1):
    #         response = requests.get(self.base_url + "/quizzes/" + str(i))
    #         print(json.loads(response.content))
    #         # self.assertEqual(response.status_code, 200)

    
    

if __name__ == "__main__":
    unittest.main()

