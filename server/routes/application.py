from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Application, Job, User

application_bp = Blueprint('application_bp', __name__)

@application_bp.route('/applications', methods=['POST'])
@jwt_required()
def create_application():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    if user.role != 'creator':
        return jsonify({'error': 'Only creators can apply for jobs'}), 403

    data = request.get_json()
    job_id = data.get('job_id')
    cover_letter = data.get('cover_letter')
    price_offer = data.get('price_offer')

    if not all([job_id, price_offer]):
        return jsonify({'error': 'Job ID and price offer required'}), 400

    job = Job.query.get_or_404(job_id)
    application = Application(cover_letter=cover_letter, price_offer=price_offer, creator_id=user_id, job_id=job_id)
    db.session.add(application)
    db.session.commit()
    return jsonify({'id': application.id, 'job_id': job_id, 'cover_letter': cover_letter, 'price_offer': price_offer}), 201

@application_bp.route('/applications', methods=['GET'])
@jwt_required()
def get_applications():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    if user.role == 'creator':
        applications = Application.query.filter_by(creator_id=user_id).all()
    else:
        jobs = Job.query.filter_by(client_id=user_id).all()
        applications = [app for job in jobs for app in job.applications]
    return jsonify([{'id': app.id, 'job_id': app.job_id, 'cover_letter': app.cover_letter, 'price_offer': app.price_offer} for app in applications]), 200