from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from utils.db import users_collection

bcrypt = Bcrypt()

def register_user(username, password):
    if users_collection.find_one({"username": username}):
        return {"error": "User already exists"}, 400
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    users_collection.insert_one({"username": username, "password": hashed_password, "role": "user"})
    return {"message": "User registered successfully"}, 201

def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.check_password_hash(user['password'], password):
        access_token = create_access_token(identity={"username": username, "role": user["role"]})
        return {"access_token": access_token}, 200
    return {"error": "Invalid credentials"}, 401
