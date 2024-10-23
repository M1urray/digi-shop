from flask import jsonify, request
from app.categories import bp
from app.model import Category, Product
from app.extensions import db

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



@bp.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    new_category = Category(name=data['name'])
    
    db.session.add(new_category)
    db.session.commit()
    
    return jsonify({"message": "Category added successfully!"}), 201
