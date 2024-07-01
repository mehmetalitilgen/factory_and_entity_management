import unittest
from app import create_app
from models import mongo
import json


class EntityTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['MONGO_URI'] = 'mongodb://localhost:27017/testdb'
        self.app.config['JWT_SECRET_KEY'] = 'test_secret'
        self.app.config['TESTING'] = True

        with self.app.app_context():
            mongo.db.users.delete_many({})
            mongo.db.entities.delete_many({})

    def tearDown(self):
        with self.app.app_context():
            mongo.db.users.delete_many({})
            mongo.db.entities.delete_many({})

    def test_create_entity(self):
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

        entity_data = {
            'name': 'Entity1',
            'factory': 'Factory1'
        }
        res = self.client.post('/entity', data=json.dumps(entity_data),
                               headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Entity created successfully', str(res.data))

    def test_get_entities(self):
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

        entity_data = {
            'name': 'Entity1',
            'factory': 'Factory1'
        }
        self.client.post('/entity', data=json.dumps(entity_data), headers={'Authorization': f'Bearer {access_token}'},
                         content_type='application/json')

        res = self.client.get('/entities?page=1&per_page=10', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('Entities retrieved successfully', str(res.data))

    def test_get_entity(self):
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

        entity_data = {
            'name': 'Entity1',
            'factory': 'Factory1'
        }
        self.client.post('/entity', data=json.dumps(entity_data), headers={'Authorization': f'Bearer {access_token}'},
                         content_type='application/json')

        entity_id = str(mongo.db.entities.find_one({'name': 'Entity1'})['_id'])
        res = self.client.get(f'/entity/{entity_id}', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('Entity retrieved successfully', str(res.data))

    def test_update_entity(self):
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

        entity_data = {
            'name': 'Entity1',
            'factory': 'Factory1'
        }
        self.client.post('/entity', data=json.dumps(entity_data), headers={'Authorization': f'Bearer {access_token}'},
                         content_type='application/json')

        entity_id = str(mongo.db.entities.find_one({'name': 'Entity1'})['_id'])
        update_data = {
            'name': 'Entity1 Updated',
            'factory': 'Factory1 Updated'
        }
        res = self.client.put(f'/entity/{entity_id}', data=json.dumps(update_data),
                              headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Entity updated successfully', str(res.data))

    def test_delete_entity(self):
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

        entity_data = {
            'name': 'Entity1',
            'factory': 'Factory1'
        }
        self.client.post('/entity', data=json.dumps(entity_data), headers={'Authorization': f'Bearer {access_token}'},
                         content_type='application/json')

        entity_id = str(mongo.db.entities.find_one({'name': 'Entity1'})['_id'])
        res = self.client.delete(f'/entity/{entity_id}', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('Entity deleted successfully', str(res.data))


if __name__ == "__main__":
    unittest.main()
