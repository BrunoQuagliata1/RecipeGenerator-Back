from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, authenticate_user

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    message, success = register_user(data['email'], data['name'], data['password'])
    if success:
        return jsonify(message), 201
    else:
        return jsonify(message), 409

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    result, success = authenticate_user(data['email'], data['password'])
    if success:
        return jsonify(result), 200
    else:
        return jsonify(result), 401
