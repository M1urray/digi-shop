import base64
from io import BytesIO
import os
from flask import jsonify, request
from app.products import bp
from app.model import Brand, Category, SubCategory, Product, Tag, Specification
from app.extensions import db
from flask import current_app
from PIL import Image


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
            'stock': product.stock,
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
        'stock': product.stock,
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



# Utility function to save base64 image
def save_base64_image(base64_string, image_name):
    try:
        # Decode the base64 string and save the image
        image_data = base64.b64decode(base64_string.split(',')[1])  # Strip the data:image/png;base64, part
        image = Image.open(BytesIO(image_data))
        
        # Ensure the 'uploads' directory exists
        uploads_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'product_images')
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        
        # Save the image with the given name
        image_path = os.path.join(uploads_dir, f"{image_name}.png")
        image.save(image_path)
        return image_path
    except Exception as e:
        raise ValueError(f"Error saving image: {str(e)}")

# Route for placing the order and handling product data
@bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    
    try:
        # Fetch the category, subcategory, and brand
        category = Category.query.get(data['category'])
        subcategory = SubCategory.query.get(data['subcategory'])
        brand = Brand.query.get(data['brand'])
        
        if not category or not subcategory or not brand:
            return jsonify({"error": "Invalid category, subcategory, or brand ID."}), 400
        
        # Create the product
        new_product = Product(
            name=data['productName'],
            price=float(data['price']),
            discount=data['discountPrice'],
            stock=int(data['stock']),
            category_id=category.id,
            subcategory_id=subcategory.id,
            brand_id=brand.id
        )
        db.session.add(new_product)
        db.session.commit()  # Save the product first to get its ID
        
        # Handle product images
        for img in data['images']:
            image_key = img['key']
            image_url = img['url']
            
            # Save the image and associate with the product
            image_path = save_base64_image(image_url, f"{new_product.id}_{image_key}")
            new_product.image = image_path  # Assign main image path to the product (or you can associate multiple images)

        # Handle specifications
        for spec in data['specifications']:
            specification = Specification(
                specification_name=spec['name'],
                specification_value=spec['value'],
                product_id=new_product.id
            )
            db.session.add(specification)

        # Handle tags
        for tag_data in data['tags']:
            tag = Tag.query.filter_by(name=tag_data['tagNames']).first()
            if not tag:
                # If tag doesn't exist, create a new one
                tag = Tag(name=tag_data['tagNames'], description=tag_data['description'])
                db.session.add(tag)
            
            # Add tag to the product
            new_product.tags.append(tag)

        db.session.commit()  # Commit all changes

        return jsonify({"message": "Product added successfully!"}), 201

    except KeyError as e:
        return jsonify({"error": f"Missing key: {e}"}), 400
    except Exception as e:
        db.session.rollback()  # Rollback any changes in case of error
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


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
            'stock': product.stock,
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
            'stock': product.stock,
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
            'stock': product.stock,
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

