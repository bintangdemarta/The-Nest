import unittest
import json
import os
import io
from app import app, db, User, File

class TestAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['UPLOAD_FOLDER'] = 'test_uploads'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
        os.makedirs('test_uploads', exist_ok=True)

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        # Clean up uploads
        import shutil
        if os.path.exists('test_uploads'):
            shutil.rmtree('test_uploads')

    def test_register(self):
        response = self.app.post('/api/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        self.app.post('/api/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        response = self.app.post('/api/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue('token' in data)
        return data['token']

    def test_upload_and_list(self):
        token = self.test_login()
        headers = {'x-access-token': token}
        
        data = {
            'file': (io.BytesIO(b'test content'), 'test_file.txt')
        }
        response = self.app.post('/api/upload', headers=headers, data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 201)
        
        response = self.app.get('/api/files', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['files']), 1)
        self.assertEqual(data['files'][0]['filename'], 'test_file.txt')

if __name__ == '__main__':
    unittest.main()
