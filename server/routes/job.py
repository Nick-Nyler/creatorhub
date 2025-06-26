from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Job, User
from datetime import datetime

job_bp = Blueprint('job_bp', __name__)

@job_bp.route('/jobs', methods=['POST'])
@jwt_required()
def create_job():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.role != 'client':
        return jsonify({'error': 'Only clients can post jobs'}), 403

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    budget = data.get('budget')
    deadline = data.get('deadline')

    if not all([title, description, budget, deadline]):
        return jsonify({'error': 'All fields required'}), 400

    try:
        deadline = datetime.fromisoformat(deadline)
    except ValueError:
        return jsonify({'error': 'Invalid deadline format'}), 400

    job = Job(title=title, description=description, budget=budget, deadline=deadline, client_id=user_id)
    db.session.add(job)
    db.session.commit()

    return jsonify({'id': job.id, 'title': job.title, 'description': job.description, 'budget': job.budget, 'deadline': job.deadline.isoformat()}), 201

@job_bp.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    return jsonify([{'id': job.id, 'title': job.title, 'description': job.description, 'budget': job.budget, 'deadline': job.deadline.isoformat(), 'client_id': job.client_id} for job in jobs]), 200

@job_bp.route('/jobs/<int:id>', methods=['GET'])
def get_job(id):
    job = Job.query.get_or_404(id)
    return jsonify({'id': job.id, 'title': job.title, 'description': job.description, 'budget': job.budget, 'deadline': job.deadline.isoformat(), 'client_id': job.client_id}), 200