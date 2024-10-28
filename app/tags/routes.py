from flask import jsonify, request
from app.tags import bp
from app.model import Product, Tag
from app.extensions import db


# Routes for managing tags
@bp.route('/product/<int:product_id>/tags', methods=['POST'])
def add_tag(product_id):
    data = request.json
    tag_name = data.get('name')
    description = data.get('description')

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    tag = Tag.query.filter_by(name=tag_name).first()
    if not tag:
        tag = Tag(name=tag_name, description=description)
        db.session.add(tag)

    product.tags.append(tag)
    db.session.commit()

    return jsonify({"message": f"Tag '{tag_name}' added to product '{product.name}'."}), 201

@bp.route('/product/<int:product_id>/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(product_id, tag_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    tag = Tag.query.get(tag_id)
    if not tag or tag not in product.tags:
        return jsonify({"error": "Tag not associated with this product"}), 404

    product.tags.remove(tag)
    db.session.commit()

    return jsonify({"message": f"Tag '{tag.name}' removed from product '{product.name}'."}), 200
