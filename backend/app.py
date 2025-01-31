import os
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from dotenv import load_dotenv
import gridfs
from flask_cors import CORS
import logging  # Add logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load secret key and database URI from environment variables
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
mongo_uri = os.getenv('MONGO_URI')

# Connect to MongoDB
try:
    client = MongoClient(mongo_uri)
    db = client['hackathon_db']
    users_collection = db['users']
    fs = gridfs.GridFS(db)  # For file storage (e.g., images, videos)
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {e}")
    raise

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username, password = data['username'], data['password']
    
    if users_collection.find_one({"username": username}):
        return jsonify({"message": "User already exists"}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    users_collection.insert_one({"username": username, "password": hashed_password, "role": "user"})
    
    return jsonify({"message": "User registered successfully"}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = users_collection.find_one({"username": username})
    
    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    # ✅ Only store the username (string) as identity
    access_token = create_access_token(identity=str(username))  

    return jsonify({"access_token": access_token}), 200



@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()  # This will now only be the username (string)
    
    if not current_user:
        return jsonify({"message": "Invalid token"}), 401

    # 🔹 Fetch user details from MongoDB
    user = users_collection.find_one({"username": current_user})
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({
        "message": f"Hello, {current_user}! You are a {user['role']}."
    }), 200

# Analyze Text (dummy endpoint for AI processing)
@app.route('/analyze-text', methods=['POST'])
@jwt_required()
def analyze_text():
    data = request.json
    text = data.get("text")
    
    # Perform AI processing here
    result = f"Processed text: {text}"
    
    return jsonify({"analysis": result}), 200

# File Upload (dummy endpoint to upload files)
@app.route('/upload-file', methods=['POST'])
@jwt_required()
def upload_file():
    file = request.files['file']
    
    # Save the file to MongoDB GridFS
    fs.put(file, filename=file.filename)
    
    return jsonify({"message": "File uploaded successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
