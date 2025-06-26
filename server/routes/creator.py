from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, PortfolioItem

creator_bp = Blueprint('creator_bp', __name__)

@creator_bp.route('/creators', methods=['GET'])
def get_creators():
    creators = User.query.filter_by(role='creator').all()
    return jsonify([{'id': c.id, 'name': c.name, 'bio': c.bio, 'skills': c.skills, 'profile_img': c.profile_img} for c in creators]), 200

@creator_bp.route('/creators/<int:id>', methods=['GET'])
def get_creator(id):
    creator = User.query.filter_by(id=id, role='creator').first_or_404()
    portfolio_items = [{'id': p.id, 'title': p.title, 'description': p.description, 'image_url': p.image_url} for p in creator.portfolio_items]
    return jsonify({'id': creator.id, 'name': creator.name, 'bio': creator.bio, 'skills': creator.skills, 'profile_img': creator.profile_img, 'portfolio_items': portfolio_items}), 200

@creator_bp.route('/creators/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    if user.role != 'creator':
        return jsonify({'error': 'Only creators can update profiles'}), 403

    data = request.get_json()
    user.bio = data.get('bio', user.bio)
    user.skills = data.get('skills', user.skills)
    user.profile_img = data.get('profile_img', user.profile_img)
    db.session.commit()
    return jsonify({'id': user.id, 'bio': user.bio, 'skills': user.skills, 'profile_img': user.profile_img}), 200

@creator_bp.route('/portfolio', methods=['POST'])
@jwt_required()
def create_portfolio_item():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    if user.role != 'creator':
        return jsonify({'error': 'Only creators can add portfolio items'}), 403

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    image_url = data.get('image_url')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    portfolio_item = PortfolioItem(title=title, description=description, image_url=image_url, creator_id=user_id)
    db.session.add(portfolio_item)
    db.session.commit()
    return jsonify({'id': portfolio_item.id, 'title': portfolio_item.title, 'description': portfolio_item.description, 'image_url': portfolio_item.image_url}), 201