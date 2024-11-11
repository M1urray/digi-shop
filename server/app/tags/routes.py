from flask import jsonify, request
from app.tags import bp
from app.model import Product, Tag
from app.extensions import db

# Retrieve all tags
@bp.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify([tag.to_dict() for tag in tags]), 200

# Add a new tag to the database
@bp.route('/tags', methods=['POST'])
def create_tag():
    data = request.json
    tag_name = data.get('name')
    description = data.get('description')

    # Check if a tag with this name already exists
    existing_tag = Tag.query.filter_by(name=tag_name).first()
    if existing_tag:
        return jsonify({"error": "Tag with this name already exists"}), 400

    # Create a new tag
    new_tag = Tag(name=tag_name, description=description)
    db.session.add(new_tag)
    db.session.commit()

    return jsonify(new_tag.to_dict()), 201

# Retrieve a specific tag by ID
@bp.route('/tags/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"error": "Tag not found"}), 404
    return jsonify(tag.to_dict()), 200

# Add a tag to a specific product
@bp.route('/product/<int:product_id>/tags', methods=['POST'])
def add_tag_to_product(product_id):
    data = request.json
    tag_name = data.get('name')
    description = data.get('description')

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Check if the tag already exists; if not, create it
    tag = Tag.query.filter_by(name=tag_name).first()
    if not tag:
        tag = Tag(name=tag_name, description=description)
        db.session.add(tag)

    # Add the tag to the product and commit
    product.tags.append(tag)
    db.session.commit()

    return jsonify({"message": f"Tag '{tag_name}' added to product '{product.name}'."}), 201

# Delete a tag from a specific product
@bp.route('/product/<int:product_id>/tags/<int:tag_id>', methods=['DELETE'])
def remove_tag_from_product(product_id, tag_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    tag = Tag.query.get(tag_id)
    if not tag or tag not in product.tags:
        return jsonify({"error": "Tag not associated with this product"}), 404

    # Remove the tag from the product
    product.tags.remove(tag)
    db.session.commit()

    return jsonify({"message": f"Tag '{tag.name}' removed from product '{product.name}'."}), 200

# Delete a tag from the database by ID
@bp.route('/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"error": "Tag not found"}), 404

    db.session.delete(tag)
    db.session.commit()

    return jsonify({"message": f"Tag '{tag.name}' deleted from database."}), 200
