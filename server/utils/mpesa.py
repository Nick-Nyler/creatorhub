import requests
import base64
import os
from datetime import datetime
from app import db
from models import Payment
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

class Mpesa:
    def __init__(self):
        self.consumer_key = os.getenv('MPESA_CONSUMER_KEY')
        self.consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
        self.shortcode = os.getenv('MPESA_SHORTCODE')
        self.passkey = os.getenv('MPESA_PASSKEY')
        self.base_url = 'https://sandbox.safaricom.co.ke'
        self.access_token = self._get_access_token()
        logger.debug(f"Initialized Mpesa with token: {self.access_token[:10]}...")

    def _get_access_token(self):
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        auth = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
        headers = {'Authorization': f'Basic {auth}'}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            token_data = response.json()
            return token_data['access_token']
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get access token: {e}")
            logger.error(f"Response text: {response.text}")
            raise
        except (KeyError, ValueError) as e:
            logger.error(f"Invalid token response: {e}")
            raise

    def initiate_payment(self, payment_id, phone_number, amount, job_id, creator_id):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{self.shortcode}{self.passkey}{timestamp}".encode()).decode()
        callback_url = os.getenv('MPESA_CALLBACK_URL', 'http://localhost:5000/api/v1/payment/callback')
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": str(amount),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": f"PAYMENT_{payment_id}",
            "TransactionDesc": f"Payment for Job {job_id}"
        }
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(f"{self.base_url}/mpesa/stkpush/v1/processrequest", json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            if response.status_code == 200:
                payment = Payment.query.get(payment_id)
                if payment:
                    payment.status = 'initiated'
                    db.session.commit()
            logger.debug(f"Payment response: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Payment initiation failed: {e}")
            logger.error(f"Response text: {response.text}")
            raise

# Singleton instance
mpesa = Mpesa()

initiate_payment = mpesa.initiate_payment