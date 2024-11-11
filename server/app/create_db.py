from app import create_app
from app.extensions import db 
from app.model import Product, Category, SubCategory, Order, OrderItem, Customer, Address 

app = create_app()

# Create the database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
