from flask import Flask, jsonify, request
from app.extensions import db
from app.brands import bp
from app.model import Brand

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

    if not data or not "name" in data:
        return jsonify({"message": "Brand name is required"}), 400

    brand_name = data["name"]

    # Check if the brand already exists
    existing_brand = Brand.query.filter_by(name=brand_name).first()
    if existing_brand:
        return jsonify({"message": "Brand already exists"}), 400

    new_brand = Brand(name=brand_name)
    db.session.add(new_brand)
    db.session.commit()

    return jsonify({"id": new_brand.id, "name": new_brand.name}), 201
