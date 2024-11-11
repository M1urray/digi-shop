from flask import jsonify, request
from app.categories import bp
from app.model import Category, SubCategory
from app.extensions import db
from flask_cors import CORS



# Retrieve all categories with subcategories
@bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        result = [
            {
                'id': category.id,
                'name': category.name,
                'ico': category.ico,
                'subcategories': [{'id': sub.id, 'name': sub.name} for sub in category.subcategories]
            } 
            for category in categories
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": "Error retrieving categories", "error": str(e)}), 500

# Add a new category
@bp.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()

    # Validate name and set default ico if missing
    if not data or "name" not in data:
        return jsonify({"message": "Category name is required"}), 400

    category_name = data["name"]
    ico = data.get("ico", "default-icon")  # Set a default value for `ico` if missing

    # Check if the category already exists
    existing_category = Category.query.filter_by(name=category_name).first()
    if existing_category:
        return jsonify({"message": "Category already exists"}), 400

    # Create and add the new category
    new_category = Category(name=category_name, ico=ico)
    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message": "Category added successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to add category", "error": str(e)}), 500


# Add subcategory to an existing category
@bp.route('/categories/<int:category_id>/subcategories', methods=['POST'])
def add_subcategory(category_id):
    data = request.get_json()

    # Validate input
    if not data or "name" not in data:
        return jsonify({"message": "Subcategory name is required"}), 400
    
    category = Category.query.get_or_404(category_id)

    # Check if the subcategory already exists within the category
    existing_subcategory = SubCategory.query.filter_by(name=data['name'].strip(), category_id=category.id).first()
    if existing_subcategory:
        return jsonify({"message": "Subcategory already exists in this category."}), 400 

    # Create and add the new subcategory
    new_subcategory = SubCategory(name=data['name'].strip(), category_id=category.id)
    try:
        db.session.add(new_subcategory)
        db.session.commit()
        return jsonify({"message": "Subcategory added successfully!", "subcategory": {"id": new_subcategory.id, "name": new_subcategory.name}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to add subcategory", "error": str(e)}), 500

# Delete a category by ID along with its subcategories and products
@bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        # Find the category by ID
        category = Category.query.get(category_id)
        
        # Check if the category exists
        if not category:
            return jsonify({"message": "Category not found"}), 404

        # Delete all subcategories and associated products under this category
        for subcategory in category.subcategories:
            for product in subcategory.products:
                db.session.delete(product)
            db.session.delete(subcategory)

        # Delete the category itself
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({"message": "Category and associated subcategories and products deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to delete category", "error": str(e)}), 500


@bp.route('/categories/count', methods=['GET'])
def get_category_count():
    try:
        # Count the number of categories
        category_count = Category.query.count()
        return jsonify({"category_count": category_count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500