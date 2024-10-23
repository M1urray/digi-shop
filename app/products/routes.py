from flask import jsonify, request
from app.products import bp
from app.model import Category, Product
from app.extensions import db

@bp.route('/products/', methods=['GET'])
def get_products():
    category_name = request.args.get('category')
    min_price = float(request.args.get('min_price'))
    max_price = float(request.args.get('max_price'))

    products = Product.query.join(Category).filter(
        Category.name == category_name,
        Product.price >= min_price,
        Product.price <= max_price
    ).all()

    result = []
    for product in products:
        result.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "brand": product.brand,
            "rating": product.rating,
            "discount": product.discount,
            "image": product.image
        })
    return jsonify({"products": result})

@bp.route('/products/<int:subcategory_id>', methods=['GET'])
def get_products_by_subcategory(subcategory_id):
    products = Product.query.filter_by(subcategory_id=subcategory_id).all()
    result = []
    for product in products:
        result.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'brand': product.brand,
            'rating': product.rating,
            'discount': product.discount,
            'image': product.image,
            'is_hot_deal': product.is_hot_deal
        })
    return jsonify(result)

@bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        price=data['price'],
        brand=data.get('brand'),
        rating=data.get('rating', None),
        discount=data.get('discount', None),
        image=data.get('image', None),
        is_hot_deal=data.get('is_hot_deal', False),
        subcategory_id=data['subcategory_id']
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({"message": "Product added successfully!"}), 201
