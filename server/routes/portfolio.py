from flask import Blueprint, request, jsonify
from app import db
from models import PortfolioItem
from flask_jwt_extended import jwt_required, get_jwt_identity

portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/api/v1/portfolio')

@portfolio_bp.route('', methods=['POST'])
@jwt_required()
def create_portfolio():
    data = request.get_json()
    user_id = get_jwt_identity()['id']
    item = PortfolioItem(title=data['title'], description=data['description'], image_url=data['image_url'], user_id=user_id)
    db.session.add(item)
    db.session.commit()
    return jsonify({'id': item.id, 'message': 'Portfolio item added'}), 201