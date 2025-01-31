from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required
from models.user_model import register_user, login_user

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/register", methods=["POST"])
def register():
    data = request.json
    return register_user(data["username"], data["password"])

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.json
    return login_user(data["username"], data["password"])
