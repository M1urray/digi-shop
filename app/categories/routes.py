from flask import jsonify, request
from app.categories import bp
from app.model import Category, SubCategory
from app.extensions import db
from flask_cors import CORS
CORS(bp)


@bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    result = []
    for category in categories:
        result.append({
            'id': category.id,
            'name': category.name,
            'ico': category.ico, 
            'subcategories': [{'id': sub.id, 'name': sub.name} for sub in category.subcategories]
        })
    return jsonify(result)

@bp.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    
    ico = data.get('ico', 'falcons')
    # check if the category already exists
    existing_category = Category.query.filter_by(name=data['name']).first()
    if existing_category:
        return jsonify({"message": "Category already exists"}), 400
    
    new_category = Category(name=data['name'], ico=ico)
    db.session.add(new_category)
    db.session.commit()
    
    return jsonify({"message": "Category added successfully!", "category": {"name": data['name'], "ico": ico}}), 201

@bp.route('/categories/<int:category_id>/subcategories', methods=['POST'])
def add_subcategory(category_id):
    data = request.get_json()

    category = Category.query.get_or_404(category_id)
    
    existing_subcategory = SubCategory.query.filter_by(name=data['name'], category_id=category.id).first()
    if existing_subcategory:
        return jsonify({"message": "Subcategory already exists in this category."}), 400 
    
    new_subcategory = SubCategory(name=data['name'], category_id=category.id)
    
    db.session.add(new_subcategory)
    db.session.commit()
    
    return jsonify({"message": "Subcategory added successfully!"}), 201


# Delete a category by ID
@bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    # Find the category by ID
    category = Category.query.get(category_id)
    
    # Check if the category exists
    if not category:
        return jsonify({"message": "Category not found"}), 404

    # Delete all subcategories and their associated products under this category
    for subcategory in category.subcategories:
        for product in subcategory.products:
            db.session.delete(product)
        db.session.delete(subcategory)
    
    # Delete the category itself
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({"message": "Category and associated subcategories and products deleted successfully"}), 200