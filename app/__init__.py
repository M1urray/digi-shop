from flask import Flask
from flask_migrate import Migrate
from flasgger import Swagger
from app.config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize the database extension
    db.init_app(app)
    
    # Initialize Swagger
    swagger = Swagger(app)

    # Import models here to ensure they are loaded for migrations
    with app.app_context():
        from app.products import bp as products_bp
        from app.hotdeals import bp as hotdeals_bp
        from app.orders import bp as orders_bp
        from app.categories import bp as categories_bp
        
        # Import your models for migration
        from app.model import Category, Product, Customer, Order, OrderItem, Address

        # Initialize the Migrate instance after importing models
        migrate = Migrate(app, db)
        
        # Register the blueprints
        app.register_blueprint(products_bp)
        app.register_blueprint(hotdeals_bp)
        app.register_blueprint(categories_bp)
        app.register_blueprint(orders_bp)

    return app
