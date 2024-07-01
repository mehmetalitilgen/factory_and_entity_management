import unittest
from app import create_app
from models import mongo
import json


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['MONGO_URI'] = 'mongodb://localhost:27017/testdb'
        self.app.config['JWT_SECRET_KEY'] = 'test_secret'
        self.app.config['TESTING'] = True

        with self.app.app_context():
            mongo.db.users.delete_many({})

    def tearDown(self):
        with self.app.app_context():
            mongo.db.users.delete_many({})

    def test_user_registration(self):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'factory': 'Factory1'
        }
        res = self.client.post('/register', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('User created successfully', str(res.data))

    def test_user_login(self):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'factory': 'Factory1'
        }
        self.client.post('/register', data=json.dumps(user_data), content_type='application/json')

        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        res = self.client.post('/login', data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Login successful', str(res.data))

    def test_get_user(self):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'factory': 'Factory1'
        }
        self.client.post('/register', data=json.dumps(user_data), content_type='application/json')

        login_res = self.client.post('/login', data=json.dumps({'username': 'testuser', 'password': 'testpassword'}),
                                     content_type='application/json')
        access_token = json.loads(login_res.data.decode())['data']['access_token']

        user_id = str(mongo.db.users.find_one({'username': 'testuser'})['_id'])
        res = self.client.get(f'/user/{user_id}', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('testuser', str(res.data))

    def test_delete_user(self):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'factory': 'Factory1'
        }
        self.client.post('/register', data=json.dumps(user_data), content_type='application/json')

        login_res = self.client.post('/login', data=json.dumps({'username': 'testuser', 'password': 'testpassword'}),
                                     content_type='application/json')
        access_token = json.loads(login_res.data.decode())['data']['access_token']

        user_id = str(mongo.db.users.find_one({'username': 'testuser'})['_id'])
        res = self.client.delete(f'/user/{user_id}', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('User deleted successfully', str(res.data))


if __name__ == "__main__":
    unittest.main()
