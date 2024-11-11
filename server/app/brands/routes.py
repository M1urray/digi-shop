from flask import jsonify, request
from app.extensions import db
from app.brands import bp
from app.model import Brand

# Retrieve all brands
@bp.route('/brands', methods=['GET'])
def get_brands():
    try:
        brands = Brand.query.all()
        brand_list = [{"id": brand.id, "name": brand.name} for brand in brands]
        return jsonify(brand_list), 200
    except Exception as e:
        return jsonify({"message": "Error retrieving brands", "error": str(e)}), 500

# Add a new brand
@bp.route('/brands', methods=['POST'])
def add_brand():
    data = request.get_json()

    # Validate the data payload
    if not data or "name" not in data:
        return jsonify({"message": "Brand name is required"}), 400

    brand_name = data["name"].strip()

    # Check if the brand already exists
    existing_brand = Brand.query.filter_by(name=brand_name).first()
    if existing_brand:
        return jsonify({"message": "Brand already exists"}), 400

    new_brand = Brand(name=brand_name)
    try:
        db.session.add(new_brand)
        db.session.commit()
        return jsonify({"id": new_brand.id, "name": new_brand.name}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to add brand", "error": str(e)}), 500

# Delete a brand by ID
@bp.route('/brands/<int:brand_id>', methods=['DELETE'])
def delete_brand(brand_id):
    try:
        # Find the brand by ID
        brand = Brand.query.get(brand_id)
        
        # Check if the brand exists
        if not brand:
            return jsonify({"message": "Brand not found"}), 404
        
        # Delete the brand from the database
        db.session.delete(brand)
        db.session.commit()
        
        return jsonify({"message": "Brand deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to delete brand", "error": str(e)}), 500
