import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestToDoApp(unittest.TestCase):

    def setUp(self):
        self.mongo_patcher = patch('db_manager.MongoClient')
        self.mock_mongo = self.mongo_patcher.start()
        self.mock_db = MagicMock()
        self.mock_mongo.return_value.__getitem__.return_value = self.mock_db
        self.mock_collection = MagicMock()
        self.mock_db.__getitem__.return_value = self.mock_collection

        from app import app as gateway_app
        from service_node import app as service_app
        from auth_utils import generate_token

        self.gateway = gateway_app.test_client()
        self.service = service_app.test_client()
        self.generate_token = generate_token

        gateway_app.testing = True
        service_app.testing = True

    def tearDown(self):
        self.mongo_patcher.stop()


    def test_token_generation(self):
        """Tests token generation"""
        token = self.generate_token('testuser')
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 10)

    def test_gateway_login_success(self):
        """Tests successful login attempt"""
        response = self.gateway.post('/login',
                                     data=json.dumps({'username': 'admin', 'password': 'admin'}),
                                     content_type='application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('token', data)

    def test_gateway_login_fail(self):
        """Tests unsuccessful login attempt"""
        response = self.gateway.post('/login',
                                     data=json.dumps({'username': 'admin', 'password': '123456'}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 401)


    def test_create_task(self):
        """Tests creating a task in the service node"""
        mock_insert_result = MagicMock()
        mock_insert_result.inserted_id = "123456789012"
        self.mock_collection.insert_one.return_value = mock_insert_result

        self.mock_collection.find_one.return_value = {
            "title": "Test Task",
            "description": "Description of a test task",
            "status": "todo"
        }

        response = self.service.post('/tasks',
                                     data=json.dumps({"title": "Test Task"}),
                                     content_type='application/json')

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], "Test Task")


if __name__ == '__main__':
    unittest.main()