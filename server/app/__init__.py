from flask import Flask
from app.config import Config
from app.extensions import db

def create_app(config_class=Config):
    # Initialize the Flask application
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize the database extension
    db.init_app(app)

    # Import models and blueprints here
    with app.app_context():
        # Blueprints
        from app.products import bp as products_bp
        from app.hotdeals import bp as hotdeals_bp
        from app.orders import bp as orders_bp
        from app.categories import bp as categories_bp
        from app.brands import bp as brands_bp
        from app.tags import bp as tags_bp
        from app.specifications import bp as specifications_bp
        from app.users import bp as users_bp

        # Import models for migrations
        from app.model import Category, Product, Customer, Order, OrderItem, Address

        # Register blueprints for modular routes
        app.register_blueprint(products_bp)
        app.register_blueprint(hotdeals_bp)
        app.register_blueprint(categories_bp)
        app.register_blueprint(orders_bp)
        app.register_blueprint(brands_bp)
        app.register_blueprint(tags_bp)
        app.register_blueprint(specifications_bp)
        app.register_blueprint(users_bp)

    return app
