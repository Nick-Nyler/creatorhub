from flask import Blueprint, request, jsonify
from app import db
from models import Payment
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.mpesa import initiate_payment  # Assume this is implemented

payment_bp = Blueprint('payment', __name__, url_prefix='/api/v1/payment')

@payment_bp.route('', methods=['POST'])
@jwt_required()
def create_payment():
    data = request.get_json()
    user_id = get_jwt_identity()['id']
    payment = Payment(phone_number=data['phone_number'], amount=data['amount'], job_id=data['job_id'], creator_id=data['creator_id'])
    db.session.add(payment)
    db.session.commit()
    initiate_payment(payment.id, data['phone_number'], data['amount'], data['job_id'], data['creator_id'])
    return jsonify({'id': payment.id, 'message': 'Payment initiated'}), 201

@payment_bp.route('/callback', methods=['POST'])
def payment_callback():
    data = request.get_json()
    logger.debug(f"Callback data: {data}")
    result_code = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
    checkout_request_id = data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
    if checkout_request_id:
        payment = Payment.query.filter_by(id=checkout_request_id).first()
        if payment:
            if result_code == 0:
                payment.status = 'completed'
            else:
                payment.status = 'failed'
            db.session.commit()
    return jsonify({'Result': {'ResultType': 0, 'ResultCode': 0, 'ResultDesc': 'Accepted'}}), 200