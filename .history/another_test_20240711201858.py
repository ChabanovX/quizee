import unittest
from flask_testing import TestCase
from config import db, 
from app import app, db, User, Note


class BaseTestCase(TestCase):
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

class UserTests(BaseTestCase):

    def test_register(self):
        response = self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User registered successfully', response.data)

    def test_login(self):
        # Register first
        self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        # Login
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in successfully', response.data)

    def test_create_note(self):
        # Register and login first
        self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        # Create a note
        response = self.client.post('/notes', json={
            'content': 'This is a test note'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Note added successfully', response.data)

if __name__ == '__main__':
    unittest.main()
