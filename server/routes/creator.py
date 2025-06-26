from flask import Blueprint, request, jsonify
from app import db
from models import User, PortfolioItem
from flask_jwt_extended import jwt_required, get_jwt_identity

creator_bp = Blueprint('creator', __name__, url_prefix='/api/v1/creators')

@creator_bp.route('', methods=['GET'])
@jwt_required()
def get_creators():
    creators = User.query.filter_by(role='creator').all()
    return jsonify([{'id': c.id, 'name': c.name, 'bio': 'Sample bio', 'skills': 'Sample skills', 'portfolio_items': [{'id': p.id, 'title': p.title, 'description': p.description, 'image_url': p.image_url} for p in c.portfolio_items]} for c in creators]), 200

@creator_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_creator(id):
    creator = User.query.get_or_404(id)
    return jsonify({'id': creator.id, 'name': creator.name, 'bio': 'Sample bio', 'skills': 'Sample skills', 'portfolio_items': [{'id': p.id, 'title': p.title, 'description': p.description, 'image_url': p.image_url} for p in creator.portfolio_items]}), 200