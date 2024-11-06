from app.extensions import db

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ico = db.Column(db.String(200), nullable=False, default="falcons")
    subcategories = db.relationship('SubCategory', backref='category', lazy=True)
    products = db.relationship('Product', backref='category', lazy=True)

class SubCategory(db.Model):
    __tablename__ = 'subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    products = db.relationship('Product', backref='subcategory', lazy=True)


class Brand(db.Model):
    __tablename__ = 'brands'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    products = db.relationship('Product', backref='brand', lazy=True)


class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)

    # Remove the `backref` in Order and explicitly declare orders here if necessary
    # orders = db.relationship('Order', lazy=True)  # Uncomment if needed
    

class Address(db.Model):
    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(200), nullable=False)
    town = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    
    # Remove the `backref` in Order and explicitly declare orders here if necessary
    # orders = db.relationship('Order', lazy=True)  # Uncomment if needed


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    notes = db.Column(db.String(500), nullable=True)
    
    # Define relationship without backref to avoid name conflicts
    customer = db.relationship('Customer', lazy=True)
    address = db.relationship('Address', lazy=True)
    items = db.relationship('OrderItem', backref='order', lazy=True)


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Association table for many-to-many relationship between Product and Tag
product_tags = db.Table(
    'product_tags',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    products = db.relationship('Product', secondary=product_tags, back_populates='tags', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }



class Specification(db.Model):
    __tablename__ = 'specifications'
    
    id = db.Column(db.Integer, primary_key=True)
    specification_name = db.Column(db.String(100), nullable=False)
    specification_value = db.Column(db.String(200), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    stock = db.Column(db.Integer, nullable=True)
    discount = db.Column(db.String(10), nullable=True)
    image = db.Column(db.String(200), nullable=True)
    is_hot_deal = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=False)
    
    # Many-to-many relationship with Tag
    tags = db.relationship('Tag', secondary=product_tags, back_populates='products', lazy=True)
    
    # One-to-many relationship with Specification
    specifications = db.relationship('Specification', backref='product', lazy=True)