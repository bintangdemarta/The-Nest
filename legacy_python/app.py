import os
import datetime
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SECRET_KEY'] = 'replace-with-a-very-hard-to-guess-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max limit

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    files = db.relationship('File', backref='owner', lazy=True)
    folders = db.relationship('Folder', backref='owner', lazy=True)

class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('folder.id'), nullable=True)
    subfolders = db.relationship('Folder', backref=db.backref('parent', remote_side=[id]), lazy=True)
    files = db.relationship('File', backref='folder', lazy=True)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False, default=0)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'), nullable=True)
    share_token = db.Column(db.String(100), unique=True, nullable=True)

# Decorator for token auth
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Routes
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    # Serve static files but exclude sensitive ones if necessary
    if path.endswith('.py') or path.endswith('.db') or path.endswith('.txt'):
         return make_response("Access denied", 403)
    return send_from_directory('.', path)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
        
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Registered successfully!'}), 201
    except:
        return jsonify({'message': 'Username already exists!'}), 400

@app.route('/api/login', methods=['POST'])
def login():
    auth = request.get_json()
    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response('Could not verify', 401)
    
    user = User.query.filter_by(username=auth['username']).first()
    if user and bcrypt.check_password_hash(user.password, auth['password']):
        token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    
    return make_response('Could not verify', 401)

@app.route('/api/upload', methods=['POST'])
@token_required
def upload_file(current_user):
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    folder_id = request.form.get('folder_id')
    
    if folder_id == 'null' or folder_id == 'undefined':
        folder_id = None

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        # Ensure user directory exists
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id))
        os.makedirs(user_folder, exist_ok=True)
        
        # Check if file already exists for this user in this folder
        existing_file = File.query.filter_by(user_id=current_user.id, filename=filename, folder_id=folder_id).first()
        if existing_file:
             return jsonify({'message': 'File already exists'}), 409

        file.save(os.path.join(user_folder, filename))
        
        file_size = os.path.getsize(os.path.join(user_folder, filename))
        new_file = File(filename=filename, owner=current_user, size=file_size, folder_id=folder_id)
        db.session.add(new_file)
        db.session.commit()
        return jsonify({'message': 'File uploaded successfully'}), 201

@app.route('/api/files', methods=['GET'])
@token_required
def get_files(current_user):
    folder_id = request.args.get('folder_id')
    search_query = request.args.get('search')

    if folder_id == 'null' or folder_id == 'undefined':
        folder_id = None
        
    query = File.query.filter_by(user_id=current_user.id)
    
    if search_query:
        query = query.filter(File.filename.ilike(f'%{search_query}%'))
    else:
        query = query.filter_by(folder_id=folder_id)
        
    files = query.all()
    
    if search_query:
        folders = [] # Don't show folders in search results for simplicity, or filter them too
    else:
        folders = Folder.query.filter_by(user_id=current_user.id, parent_id=folder_id).all()
    
    output = {'files': [], 'folders': []}
    
    for folder in folders:
        folder_data = {
            'id': folder.id,
            'name': folder.name,
            'type': 'folder'
        }
        output['folders'].append(folder_data)

    for file in files:
        file_data = {
            'id': file.id,
            'filename': file.filename,
            'size': file.size,
            'upload_date': file.upload_date.isoformat(),
            'type': 'file'
        }
        output['files'].append(file_data)
    return jsonify(output)

@app.route('/api/folders', methods=['POST'])
@token_required
def create_folder(current_user):
    data = request.get_json()
    name = data.get('name')
    parent_id = data.get('parent_id')
    
    if not name:
        return jsonify({'message': 'Folder name required'}), 400
        
    new_folder = Folder(name=name, owner=current_user, parent_id=parent_id)
    db.session.add(new_folder)
    db.session.commit()
    return jsonify({'message': 'Folder created'}), 201

@app.route('/api/files/<int:file_id>', methods=['GET'])
@token_required
def get_file_details(current_user, file_id):
    file = File.query.filter_by(user_id=current_user.id, id=file_id).first()
    if not file:
        return jsonify({'message': 'File not found'}), 404
    
    file_data = {
        'id': file.id,
        'filename': file.filename,
        'size': file.size,
        'upload_date': file.upload_date.isoformat(),
        'share_token': file.share_token
    }
    return jsonify(file_data)

@app.route('/api/files/<int:file_id>/share', methods=['POST'])
@token_required
def share_file(current_user, file_id):
    file = File.query.filter_by(user_id=current_user.id, id=file_id).first()
    if not file:
        return jsonify({'message': 'File not found'}), 404
    
    if not file.share_token:
        file.share_token = str(uuid.uuid4())
        db.session.commit()
        
    return jsonify({'share_token': file.share_token})

@app.route('/shared/<token>', methods=['GET'])
def download_shared_file(token):
    file = File.query.filter_by(share_token=token).first()
    if not file:
        return jsonify({'message': 'File not found or link expired'}), 404
        
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(file.user_id))
    return send_from_directory(user_folder, file.filename, as_attachment=True)

@app.route('/api/download/<filename>', methods=['GET'])
@token_required
def download_file(current_user, filename):
    file = File.query.filter_by(user_id=current_user.id, filename=filename).first()
    if not file:
        return jsonify({'message': 'File not found'}), 404
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id))
    return send_from_directory(user_folder, filename, as_attachment=True)

@app.route('/api/files/<filename>', methods=['DELETE'])
@token_required
def delete_file(current_user, filename):
    file = File.query.filter_by(user_id=current_user.id, filename=filename).first()
    if not file:
        return jsonify({'message': 'File not found'}), 404
    
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id))
    file_path = os.path.join(user_folder, filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        
    db.session.delete(file)
    db.session.commit()
    db.session.delete(file)
    db.session.commit()
    return jsonify({'message': 'File deleted'})

@app.route('/api/swagger.json')
def swagger_spec():
    return jsonify({
        "swagger": "2.0",
        "info": {
            "title": "The Nest API",
            "version": "1.0.0",
            "description": "API documentation for The Nest Personal Cloud"
        },
        "basePath": "/api",
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "x-access-token",
                "in": "header"
            }
        },
        "security": [{"Bearer": []}],
        "paths": {
            "/files": {
                "get": {
                    "summary": "List files",
                    "parameters": [
                        {"name": "folder_id", "in": "query", "type": "integer"},
                        {"name": "search", "in": "query", "type": "string"}
                    ],
                    "responses": {
                        "200": {"description": "List of files and folders"}
                    }
                }
            },
            "/upload": {
                "post": {
                    "summary": "Upload file",
                    "consumes": ["multipart/form-data"],
                    "parameters": [
                        {"name": "file", "in": "formData", "type": "file", "required": True},
                        {"name": "folder_id", "in": "formData", "type": "integer"}
                    ],
                    "responses": {
                        "201": {"description": "File uploaded"}
                    }
                }
            }
            # Add more endpoints as needed
        }
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
