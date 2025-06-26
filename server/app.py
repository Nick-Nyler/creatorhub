from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions globally
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///creatorhub.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.job import job_bp
    from routes.creator import creator_bp
    from routes.payment import payment_bp
    from routes.portfolio import portfolio_bp
    from routes.application import application_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(creator_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(application_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)