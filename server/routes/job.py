from flask import Blueprint, request, jsonify
from app import db
from models import Job
from flask_jwt_extended import jwt_required, get_jwt_identity

job_bp = Blueprint('job', __name__, url_prefix='/api/v1/jobs')

@job_bp.route('', methods=['GET'])
@jwt_required()
def get_jobs():
    jobs = Job.query.all()
    return jsonify([{'id': j.id, 'title': j.title, 'description': j.description, 'budget': j.budget, 'deadline': j.deadline.isoformat()} for j in jobs]), 200

@job_bp.route('', methods=['POST'])
@jwt_required()
def create_job():
    data = request.get_json()
    user_id = get_jwt_identity()['id']
    job = Job(title=data['title'], description=data['description'], budget=data['budget'], deadline=data['deadline'], client_id=user_id)
    db.session.add(job)
    db.session.commit()
    return jsonify({'id': job.id, 'message': 'Job created'}), 201