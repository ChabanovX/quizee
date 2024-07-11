response = requests.post(self.base_url + "/create_quiz", json={
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
        self.assertEqual(response.status_code, 201)


