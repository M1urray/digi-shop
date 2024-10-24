from flask import jsonify, request
from app.categories import bp
from app.model import Category, SubCategory
from app.extensions import db

# Get all categories and their subcategories
@bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    result = []
    for category in categories:
        result.append({
            'id': category.id,
            'name': category.name,
            'subcategories': [{'id': sub.id, 'name': sub.name} for sub in category.subcategories]
        })
    return jsonify(result)

# Add a new category
@bp.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    
    # Create a new Category
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    
    return jsonify({"message": "Category added successfully!"}), 201

@bp.route('/categories/<int:category_id>/subcategories', methods=['POST'])
def add_subcategory(category_id):
    data = request.get_json()

    # Find the parent category
    category = Category.query.get_or_404(category_id)
    
    # Check if the subcategory already exists under the given category
    existing_subcategory = SubCategory.query.filter_by(name=data['name'], category_id=category.id).first()
    if existing_subcategory:
        return jsonify({"message": "Subcategory already exists in this category."}), 400  # Bad Request
    
    # Create a new SubCategory linked to the Category if it doesn't exist
    new_subcategory = SubCategory(name=data['name'], category_id=category.id)
    
    db.session.add(new_subcategory)
    db.session.commit()
    
    return jsonify({"message": "Subcategory added successfully!"}), 201

