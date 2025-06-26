from flask import Blueprint, request, jsonify
from app import db
from models import User
from flask_jwt_extended import create_access_token
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1')

@auth_bp.route('/signup', methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    logger.debug(f"Signup data: {data}")
    user = User(name=data['name'], email=data['email'], password=data['password'], role=data['role'])
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity={'id': user.id, 'email': user.email})
    return jsonify({'access_token': token, 'user': {'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role}}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.password == data['password']:  # Use hashing in production
        token = create_access_token(identity={'id': user.id, 'email': user.email})
        return jsonify({'access_token': token, 'user': {'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role}}), 200
    return jsonify({'error': 'Invalid credentials'}), 401