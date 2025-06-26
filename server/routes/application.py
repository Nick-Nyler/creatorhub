from flask import Blueprint, request, jsonify
from app import db
from models import Application
from flask_jwt_extended import jwt_required, get_jwt_identity

application_bp = Blueprint('application', __name__, url_prefix='/api/v1/applications')

@application_bp.route('', methods=['POST'])
@jwt_required()
def create_application():
    data = request.get_json()
    user_id = get_jwt_identity()['id']
    app = Application(cover_letter=data['cover_letter'], price_offer=data['price_offer'], job_id=data['job_id'], creator_id=user_id)
    db.session.add(app)
    db.session.commit()
    return jsonify({'id': app.id, 'message': 'Application submitted'}), 201