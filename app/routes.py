from flask import Blueprint, request, jsonify
from app import models
from app.utils import hash_password, verify_password

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return "User Management System"

@bp.route('/users', methods=['GET'])
def get_users():
    users = models.get_all_users()
    return jsonify([dict(user) for user in users]), 200

@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = models.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(dict(user)), 200

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    password_hash = hash_password(password)
    models.create_user(name, email, password_hash)
    return jsonify({"message": "User created"}), 201

@bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not all([name, email]):
        return jsonify({"error": "Invalid data"}), 400

    if not models.get_user_by_id(user_id):
        return jsonify({"error": "User not found"}), 404

    models.update_user(user_id, name, email)
    return jsonify({"message": "User updated"}), 200

@bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not models.get_user_by_id(user_id):
        return jsonify({"error": "User not found"}), 404

    models.delete_user(user_id)
    return jsonify({"message": "User deleted"}), 200

@bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Missing 'name' parameter"}), 400

    users = models.search_users_by_name(name)
    return jsonify([dict(user) for user in users]), 200

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"error": "Missing credentials"}), 400

    user = models.login_user(email, password)
    if user and verify_password(password, user['password']):
        return jsonify({"status": "success", "user_id": user['id']}), 200
    return jsonify({"status": "failed"}), 401
