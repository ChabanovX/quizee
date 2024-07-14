# Quizee API

## Project Description
This is a backend API for creating and managing quizzes. This API allows users to register, log in, and manage their quizzes securely using JWT authentication. The project is built using Flask, Flask-RESTX, and SQLAlchemy, providing a robust framework for developing and maintaining the application.

## Feature List
- **User Authentication**: Secure user registration and login using JWT tokens.
- **Quiz Management**: Create, view, and delete quizzes.
- **Question and Answer Handling**: Add questions and multiple-choice answers to quizzes.
- **Profile Management**: View user profile information.
- **API Documentation**: Interactive API documentation using Swagger (Flask-RESTX).

## Demo
Screenshots of the API in action:

**Swagger UI**:
![Swagger UI](https://your-image-link.com/swagger-ui.png)

## Live Demo
Check out the live version of the Quizee [here](https://drive.google.com/file/d/1wJ5IRnerl_Ti9Pl26eQNZWYqRVSz2UaZ/view?usp=sharing).

## Usage Instructions
### User Guide
1. **Register a new user**:
   - Endpoint: `/auth/register`
   - Method: `POST`
   - Payload: `{"email": "user@example.com", "username": "user", "password": "password"}`

2. **Login to get a JWT token**:
   - Endpoint: `/auth/login`
   - Method: `POST`
   - Payload: `{"username": "user", "password": "password"}`

3. **Create a new quiz**:
   - Endpoint: `/quiz/create_quiz`
   - Method: `POST`
   - Headers: `{"Authorization": "Bearer <your_token>"}`
   - Payload: `{"naming": "Quiz Name", "questions": [{"text": "Question 1", "answers": [{"text": "Answer 1", "is_correct": true}, {"text": "Answer 2", "is_correct": false}], "hasMultipleRightAnswers": false}]}`

4. **View all quizzes**:
   - Endpoint: `/quiz/quizzes`
   - Method: `GET`
   - Headers: `{"Authorization": "Bearer <your_token>"}`

5. **Delete a quiz**:
   - Endpoint: `/quiz/delete_quiz/<quiz_id>`
   - Method: `DELETE`
   - Headers: `{"Authorization": "Bearer <your_token>"}`

## Installation / Deployment Instructions
1. **Clone the repository**:
   ```bash
   git clone https://your-repo-link.com
   cd your-repo
   ```
2. **Install Dependencies**
xxx

