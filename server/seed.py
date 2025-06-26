from app import create_app, db
from models import User, Job, PortfolioItem, Application, Payment
from datetime import datetime

app = create_app()
with app.app_context():
    db.session.query(Payment).delete()
    db.session.query(Application).delete()
    db.session.query(PortfolioItem).delete()
    db.session.query(Job).delete()
    db.session.query(User).delete()
    db.session.commit()

    client1 = User(name="John Doe", email="john.doe@example.com", password="password123", role="client")
    creator1 = User(name="Jane Smith", email="jane.smith@example.com", password="password123", role="creator")
    creator2 = User(name="Mike Johnson", email="mike.johnson@example.com", password="password123", role="creator")
    db.session.add_all([client1, creator1, creator2])
    db.session.commit()

    job1 = Job(title="Design Website Homepage", description="Create a modern homepage", budget=200.0, deadline=datetime(2025, 7, 5), client_id=client1.id)
    job2 = Job(title="Write Blog Post", description="Write a 1000-word blog post", budget=50.0, deadline=datetime(2025, 7, 1), client_id=client1.id)
    db.session.add_all([job1, job2])
    db.session.commit()

    portfolio1 = PortfolioItem(title="E-commerce Website", description="Responsive site", image_url="https://example.com/ecommerce.jpg", user_id=creator1.id)
    portfolio2 = PortfolioItem(title="AI Article Series", description="Three-part series", image_url="https://example.com/ai.jpg", user_id=creator2.id)
    db.session.add_all([portfolio1, portfolio2])
    db.session.commit()

    application1 = Application(cover_letter="Excited to design", price_offer=180.0, job_id=job1.id, creator_id=creator1.id)
    application2 = Application(cover_letter="Experienced writer", price_offer=45.0, job_id=job2.id, creator_id=creator2.id)
    db.session.add_all([application1, application2])
    db.session.commit()

    payment1 = Payment(phone_number="+254712345678", amount=180.0, status="pending", job_id=job1.id, creator_id=creator1.id)
    db.session.add(payment1)
    db.session.commit()

    print("Database seeded on Render!")