import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import Question, Category ,db

from settings import *



database_name = 'trivia'
database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER,DB_PASSWORD,'localhost:5432', database_name)


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
   
    
    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_paginated_questions(self):
        with self.app.app_context():
            res = self.client.get('/questions')
            data = json.loads(res.data)

            # Check if the response status code is 200 (OK)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)

            # Check if the 'total_questions' in the response is not empty
            self.assertTrue(data['total_questions'])

            # Check if the 'questions' in the response contains at least one question
            self.assertTrue(len(data['questions']) > 0)

            # Check if the 'categories' in the response is not empty 
            self.assertTrue(len(data['categories']) > 0)

    def test_404_sent_requesting_questions(self):
        with self.app.app_context():
            res = self.client.get('/questions?page=1000')
            data = json.loads(res.data)

            # Check if the response status code is 404 (Not Found)
            self.assertEqual(res.status_code, 404)
            # Check if the 'success' in the response is False
            self.assertEqual(data['success'], False)
            # Check if the 'message' in the response contains the expected error message
            self.assertEqual(data['message'], 'Resource not found')

    def test_get_categories(self):
        with self.app.app_context():
            res = self.client.get('/categories')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            # Check if the 'categories' in the response is not empty
            self.assertTrue(len(data['categories']) > 0)

    def test_404_get_category(self):
        with self.app.app_context():
            res = self.client.get('/categories/858585855')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Resource not found')

    def test_delete_question(self):
        with self.app.app_context():
            # Create a new question and insert it into the database
            question = Question(question='whats 1+1 ?', answer='2',
                                difficulty=1, category=1)
            question.insert()
            
            # Get the ID of the inserted question
            question_id = question.id

            # Send a DELETE request to delete the question
            res = self.client.delete(f'/questions/{question_id}')
            data = json.loads(res.data)

            deleted_question = Question.query.get(question_id)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'], str(question_id))
            self.assertIsNone(deleted_question)

    def test_422_delete_question(self):
        with self.app.app_context():
            res = self.client.delete('/questions/1')
            data = json.loads(res.data)

            # Check if the response status code is 422 (Unprocessable Entity)
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unprocessable entity')

    def test_create_question(self):
        with self.app.app_context():
        # Define a new question as a dictionary
            new_question = {
                'question': 'whats 1+1 ?',
                'answer': '2',
                'difficulty': 1,
                'category': 1
            }
            # Get the total number of questions before adding a new one
            total_questions_before = len(Question.query.all())

            res = self.client.post('/questions', json=new_question)
            data = json.loads(res.data)

            total_questions_after = len(Question.query.all())

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)
            self.assertEqual(total_questions_after, total_questions_before + 1)

    def test_422_create_question(self):
        with self.app.app_context():
            # Define a new question with missing 'difficulty' field (should result in 422 error)
            new_question = {
                'question': 'new_question',
                'answer': 'new_answer',
                'category': 1
            }
            res = self.client.post('/questions', json=new_question)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertEqual(data["success"], False)
            self.assertEqual(data["message"], "Unprocessable entity")

    def test_search_questions(self):
        with self.app.app_context():
            # Define a search term as a dictionary
            new_search = {'searchTerm': '1'}

            res = self.client.post('/questions/search', json=new_search)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertIsNotNone(data['questions'])
            self.assertIsNotNone(data['total_questions'])

    def test_404_search_question(self):
        with self.app.app_context():
            # Define an empty search term (should result in a 404 error)
            new_search = {
                'searchTerm': '',
            }

            res = self.client.post('/questions/search', json=new_search)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data["success"], False)
            self.assertEqual(data["message"], "Resource not found")

    def test_questions_per_category(self):
        with self.app.app_context():
            res = self.client.get('/categories/1/questions')
            data = json.loads(res.data)
    
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(len(data['questions']) > 0)
            self.assertTrue(data['total_questions'])
            self.assertTrue(data['current_category'])

    def test_404_get_questions_per_category(self):
        with self.app.app_context():
            res = self.client.get('/categories/a/questions')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data["success"], False)
            self.assertEqual(data["message"], "Resource not found")


    def test_play_quiz(self):
        with self.app.app_context():
            new_quiz_round = {
                'previous_questions': [],
                'quiz_category': {'type': 'Entertainment', 'id': 5}
            }

            res = self.client.post('/quizzes', json=new_quiz_round)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)

    def test_404_play_quiz(self):
        with self.app.app_context():
            new_quiz_round = {
                'previous_questions': []
            }

            res = self.client.post('/quizzes', json=new_quiz_round)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertEqual(data["success"], False)
            self.assertEqual(data["message"], "Unprocessable entity")
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()