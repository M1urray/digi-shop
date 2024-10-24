from flask import jsonify, request
from app.products import bp
from app.model import Brand, Category, SubCategory, Product
from app.extensions import db

# Get products filtered by category and price range
@bp.route('/products', methods=['GET'])
def get_products():
    category_name = request.args.get('category')
    subcategory_name = request.args.get('subcategory')  # Optional: filter by subcategory
    min_price = float(request.args.get('min_price', 0))  # Default to 0 if not provided
    max_price = float(request.args.get('max_price', float('inf')))  # Default to infinity if not provided

    # Querying based on category and price range
    query = Product.query.join(SubCategory).join(Category).filter(
        Product.price >= min_price,
        Product.price <= max_price
    )

    if category_name:
        query = query.filter(Category.name == category_name)

    if subcategory_name:
        query = query.filter(SubCategory.name == subcategory_name)

    products = query.all()

    result = []
    for product in products:
        result.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "brand": product.brand.name,  # Get the brand name
            "rating": product.rating,
            "discount": product.discount,
            "image": product.image,
            "subcategory_id": product.subcategory_id,
            "subcategory_name": product.subcategory.name,  # Get the subcategory name
            "category_id": product.category_id,  # Include category ID
            "category_name": product.subcategory.category.name  # Get the category name
        })
    return jsonify({"products": result})


# Get products by subcategory ID
@bp.route('/products/<int:subcategory_id>', methods=['GET'])
def get_products_by_subcategory(subcategory_id):
    products = Product.query.filter_by(subcategory_id=subcategory_id).all()
    subcategory = SubCategory.query.get_or_404(subcategory_id)  # Fetch the subcategory name using ID
    result = []
    
    for product in products:
        result.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'brand': product.brand.name,  # Get the brand name
            'rating': product.rating,
            'discount': product.discount,
            'image': product.image,
            'is_hot_deal': product.is_hot_deal,
            'subcategory_name': subcategory.name,  # Include the subcategory name
            'category_id': subcategory.category_id,  # Include the category ID
            'category_name': subcategory.category.name  # Include the category name
        })
    return jsonify(result)


# Add a new product
@bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()

    # Ensure required fields are provided
    name = data.get('name')
    price = data.get('price')
    brand_id = data.get('brand_id')
    subcategory_id = data.get('subcategory_id')

    if not all([name, price, brand_id, subcategory_id]):
        return jsonify({"message": "Name, price, brand_id, and subcategory_id are required."}), 400

    # Check if the subcategory exists
    subcategory = SubCategory.query.get_or_404(subcategory_id)

    # Check if the brand exists
    brand = Brand.query.get_or_404(brand_id)

    new_product = Product(
        name=name,
        price=price,
        brand_id=brand.id,  # Ensure brand_id is provided
        rating=data.get('rating', None),
        discount=data.get('discount', None),
        image=data.get('image', None),
        is_hot_deal=data.get('is_hot_deal', False),
        subcategory_id=subcategory.id,  # Use the validated subcategory id
        category_id=subcategory.category_id  # Link to the main category via the subcategory
    )
    
    # Add the new product to the session and commit it to the database
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({"message": "Product added successfully!"}), 201