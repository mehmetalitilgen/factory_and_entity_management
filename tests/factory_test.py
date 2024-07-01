import unittest
from app import create_app
from models import mongo
import json


class FactoryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['MONGO_URI'] = 'mongodb://localhost:27017/testdb'
        self.app.config['JWT_SECRET_KEY'] = 'test_secret'
        self.app.config['TESTING'] = True

        with self.app.app_context():
            mongo.db.users.delete_many({})
            mongo.db.factories.delete_many({})

    def tearDown(self):
        with self.app.app_context():
            mongo.db.users.delete_many({})
            mongo.db.factories.delete_many({})

    def test_create_factory(self):
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

        factory_data = {
            'name': 'Factory1',
            'location': 'Location1',
            'capacity': 100
        }
        res = self.client.post('/factory', data=json.dumps(factory_data),
                               headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Factory created successfully', str(res.data))

    def test_get_factories(self):
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

        factory_data = {
            'name': 'Factory1',
            'location': 'Location1',
            'capacity': 100
        }
        self.client.post('/factory', data=json.dumps(factory_data), headers={'Authorization': f'Bearer {access_token}'},
                         content_type='application/json')

        res = self.client.get('/factories?page=1&per_page=10', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('Factories retrieved successfully', str(res.data))

    def test_get_factory(self):
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

        factory_data = {
            'name': 'Factory1',
            'location': 'Location1',
            'capacity': 100
        }
        self.client.post('/factory', data=json.dumps(factory_data), headers={'Authorization': f'Bearer {access_token}'},
                         content_type='application/json')

        factory_id = str(mongo.db.factories.find_one({'name': 'Factory1'})['_id'])
        res = self.client.get(f'/factory/{factory_id}', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('Factory retrieved successfully', str(res.data))

    def test_update_factory(self):
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

        factory_data = {
            'name': 'Factory1',
            'location': 'Location1',
            'capacity': 100
        }
        self.client.post('/factory', data=json.dumps(factory_data), headers={'Authorization': f'Bearer {access_token}'},
                         content_type='application/json')

        factory_id = str(mongo.db.factories.find_one({'name': 'Factory1'})['_id'])
        update_data = {
            'name': 'Factory1 Updated',
            'location': 'Location1 Updated',
            'capacity': 200
        }
        res = self.client.put(f'/factory/{factory_id}', data=json.dumps(update_data),
                              headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Factory updated successfully', str(res.data))

    def test_delete_factory(self):
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

        factory_data = {
            'name': 'Factory1',
            'location': 'Location1',
            'capacity': 100
        }
        self.client.post('/factory', data=json.dumps(factory_data), headers={'Authorization': f'Bearer {access_token}'},
                         content_type='application/json')

        factory_id = str(mongo.db.factories.find_one({'name': 'Factory1'})['_id'])
        res = self.client.delete(f'/factory/{factory_id}', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('Factory deleted successfully', str(res.data))


if __name__ == "__main__":
    unittest.main()
