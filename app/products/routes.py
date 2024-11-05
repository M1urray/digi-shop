from flask import jsonify, request
from app.products import bp
from app.model import Brand, Category, SubCategory, Product, Tag, Specification
from app.extensions import db
from flask_cors import CORS


# Get products filtered by category, subcategory, and price range
@bp.route('/products', methods=['GET'])
def get_products():
    category_name = request.args.get('category')
    subcategory_name = request.args.get('subcategory')  # Optional: filter by subcategory
    min_price = float(request.args.get('min_price', 0))  # Default to 0 if not provided
    max_price = float(request.args.get('max_price', float('inf')))  # Default to infinity if not provided

    # Query based on category and price range
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
            "category_name": product.subcategory.category.name,  # Get the category name
            "tags": [{"id": tag.id, "name": tag.name} for tag in product.tags],  # List of tags
            "specifications": [
                {"name": spec.specification_name, "value": spec.specification_value}
                for spec in product.specifications
            ]  # List of specifications
        })
    return jsonify({"products": result})


# Get product by product ID
@bp.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get_or_404(product_id)
    subcategory = product.subcategory  # Assuming the Product model has a subcategory relationship

    result = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'brand': product.brand.name,
        'rating': product.rating,
        'discount': product.discount,
        'image': product.image,
        'is_hot_deal': product.is_hot_deal,
        'subcategory_name': subcategory.name,
        'category_id': subcategory.category_id,
        'category_name': subcategory.category.name,
        'tags': [{"id": tag.id, "name": tag.name, "description": tag.description} for tag in product.tags],
        'specifications': [
            {"name": spec.specification_name, "value": spec.specification_value}
            for spec in product.specifications
        ]
    }
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

    # Check if the subcategory and brand exist
    subcategory = SubCategory.query.get_or_404(subcategory_id)
    brand = Brand.query.get_or_404(brand_id)

    new_product = Product(
        name=name,
        price=price,
        brand_id=brand.id,
        rating=data.get('rating', None),
        discount=data.get('discount', None),
        image=data.get('image', None),
        is_hot_deal=data.get('is_hot_deal', False),
        subcategory_id=subcategory.id,
        category_id=subcategory.category_id
    )
    
    # Handle tags if provided
    tag_ids = data.get('tag_ids', [])
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_product.tags.extend(tags)

    # Handle specifications if provided
    specifications = data.get('specifications', [])
    for spec in specifications:
        specification = Specification(
            specification_name=spec['name'],
            specification_value=spec['value'],
            product=new_product
        )
        db.session.add(specification)
    
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({"message": "Product added successfully!"}), 201


# Delete a product by ID
@bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully!"}), 200

# Get products by subcategory name
@bp.route('/products/<string:category_name>/<string:subcategory_name>', methods=['GET'])
def get_products_by_subcategory_name(category_name, subcategory_name):
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        return jsonify({"message": "Category not found"}), 404

    subcategory = SubCategory.query.filter_by(name=subcategory_name, category_id=category.id).first()
    if not subcategory:
        return jsonify({"message": "Subcategory not found"}), 404

    products = Product.query.filter_by(subcategory_id=subcategory.id).all()
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
            'category_id': category.id,  # Include the category ID
            'category_name': category.name  # Include the category name
        })
    return jsonify(result)

# get product by product cartegory name
@bp.route('/products/<string:category_name>', methods=['GET'])
def get_products_by_category(category_name):
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        return jsonify({"message": "Category not found"}), 404

    products = Product.query.filter_by(category_id=category.id).all()
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
            'subcategory_name': product.subcategory.name,  # Include the subcategory name
            'category_id': category.id,  # Include the category ID
            'category_name': category.name  # Include the category name
        })
    return jsonify(result)

# get products/all with tags and specifications
@bp.route('/products/all', methods=['GET'])
def get_all_products():
    products = Product.query.all()
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
            'subcategory_name': product.subcategory.name,  # Include the subcategory name
            'category_id': product.category_id,  # Include the category ID
            'category_name': product.subcategory.category.name,  # Include the category name
            'tags': [{"id": tag.id, "name": tag.name,  "description": tag.description } for tag in product.tags],  # List of tags
            'specifications': [
                {"name": spec.specification_name, "value": spec.specification_value}
                for spec in product.specifications
            ]  # List of specifications
        })
    return jsonify(result)

