from flask import Blueprint, request, jsonify
from models.ai_model import analyze_text
from flask_jwt_extended import jwt_required

ai_routes = Blueprint("ai", __name__)

@ai_routes.route("/analyze", methods=["POST"])
@jwt_required()
def analyze():
    text = request.json["text"]
    result = analyze_text(text)
    return jsonify(result)
