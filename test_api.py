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
            db.drop_all()
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
        self.assertEqual(data['files'][0]['size'], 12) # 'test content' is 12 bytes
        self.assertTrue('upload_date' in data['files'][0])
        
        # Test details endpoint
        file_id = data['files'][0]['id']
        response = self.app.get(f'/api/files/{file_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['filename'], 'test_file.txt')
        self.assertEqual(data['size'], 12)

    def test_folders_and_sharing(self):
        token = self.test_login()
        headers = {'x-access-token': token}
        
        # Create folder
        response = self.app.post('/api/folders', headers=headers, json={'name': 'My Folder'})
        self.assertEqual(response.status_code, 201)
        
        # Get folders
        response = self.app.get('/api/files', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(len(data['folders']), 1)
        self.assertEqual(data['folders'][0]['name'], 'My Folder')
        folder_id = data['folders'][0]['id']
        
        # Upload file to folder
        data = {
            'file': (io.BytesIO(b'file in folder'), 'nested.txt'),
            'folder_id': folder_id
        }
        response = self.app.post('/api/upload', headers=headers, data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 201)
        
        # List files in folder
        response = self.app.get(f'/api/files?folder_id={folder_id}', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(len(data['files']), 1)
        self.assertEqual(data['files'][0]['filename'], 'nested.txt')
        
        # Share file
        file_id = data['files'][0]['id']
        response = self.app.post(f'/api/files/{file_id}/share', headers=headers)
        self.assertEqual(response.status_code, 200)
        share_data = json.loads(response.data)
        self.assertTrue('share_token' in share_data)
        token = share_data['share_token']
        
        # Download shared file
        response = self.app.get(f'/shared/{token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'file in folder')

if __name__ == '__main__':
    unittest.main()
