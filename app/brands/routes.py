from flask import jsonify, request
from app.extensions import db
from app.brands import bp
from app.model import Brand
from flask_cors import CORS
CORS(bp)


# Retrieve all brands
@bp.route('/brands', methods=['GET'])
def get_brands():
    brands = Brand.query.all()
    brand_list = [{"id": brand.id, "name": brand.name} for brand in brands]
    return jsonify(brand_list), 200

# Add a new brand
@bp.route('/brands', methods=['POST'])
def add_brand():
    data = request.get_json()

    # Check if the brand already exists
    existing_brand = Brand.query.filter_by(name=brand_name).first()
    if existing_brand:
        return jsonify({"message": "Brand already exists"}), 400


    if not data or not "name" in data:
        return jsonify({"message": "Brand name is required"}), 400

    brand_name = data["name"]



    new_brand = Brand(name=brand_name)
    db.session.add(new_brand)
    db.session.commit()

    return jsonify({"id": new_brand.id, "name": new_brand.name}), 201

# Delete a brand by ID
@bp.route('/brands/<int:brand_id>', methods=['DELETE'])
def delete_brand(brand_id):
    # Find the brand by ID
    brand = Brand.query.get(brand_id)
    
    # Check if the brand exists
    if not brand:
        return jsonify({"message": "Brand not found"}), 404
    
    # Delete the brand from the database
    db.session.delete(brand)
    db.session.commit()
    
    return jsonify({"message": "Brand deleted successfully"}), 200
