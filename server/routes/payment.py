from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Payment, User, Job
from utils.mpesa import stk_push

payment_bp = Blueprint('payment_bp', __name__)

@payment_bp.route('/payment', methods=['POST'])
@jwt_required()
def create_payment():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    if user.role != 'client':
        return jsonify({'error': 'Only clients can initiate payments'}), 403

    data = request.get_json()
    phone = data.get('phone_number')
    amount = data.get('amount')
    job_id = data.get('job_id')
    creator_id = data.get('creator_id')

    if not all([phone, amount, job_id, creator_id]):
        return jsonify({'error': 'All fields required'}), 400

    job = Job.query.get_or_404(job_id)
    if job.client_id != user_id:
        return jsonify({'error': 'Unauthorized to pay for this job'}), 403

    payment = Payment(amount=amount, phone_number=phone, job_id=job_id, creator_id=creator_id)
    db.session.add(payment)
    db.session.commit()

    response = stk_push(phone, amount)
    if 'ResponseCode' in response and response['ResponseCode'] == '0':
        return jsonify({'message': 'Payment request sent', 'payment_id': payment.id}), 200
    return jsonify({'error': 'Payment initiation failed', 'details': response}), 400

@payment_bp.route('/payment/callback', methods=['POST'])
def payment_callback():
    data = request.get_json()
    # Process M-Pesa callback (update payment status)
    # Note: Implement actual callback logic based on M-Pesa response
    return jsonify({'message': 'Callback received'}), 200