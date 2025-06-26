from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restful import Api
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///creatorhub.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
api = Api(app)

# Import and register blueprints
from routes.auth import auth_bp
from routes.job import job_bp
from routes.creator import creator_bp
from routes.application import application_bp
from routes.payment import payment_bp

app.register_blueprint(auth_bp, url_prefix='/api/v1')
app.register_blueprint(job_bp, url_prefix='/api/v1')
app.register_blueprint(creator_bp, url_prefix='/api/v1')
app.register_blueprint(application_bp, url_prefix='/api/v1')
app.register_blueprint(payment_bp, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run(debug=True)