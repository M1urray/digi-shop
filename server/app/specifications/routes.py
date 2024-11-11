from flask import jsonify, request
from app.hotdeals import bp
from app.model import Product, Specification, Tag
from app.extensions import db


# Routes for managing specifications
@bp.route('/product/<int:product_id>/specifications', methods=['POST'])
def add_specification(product_id):
    data = request.json
    spec_name = data.get('specification_name')
    spec_value = data.get('specification_value')

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    specification = Specification(specification_name=spec_name, specification_value=spec_value, product=product)
    db.session.add(specification)
    db.session.commit()

    return jsonify({"message": f"Specification '{spec_name}' added to product '{product.name}'."}), 201

@bp.route('/product/<int:product_id>/specifications/<int:spec_id>', methods=['DELETE'])
def delete_specification(product_id, spec_id):
    specification = Specification.query.get(spec_id)
    if not specification or specification.product_id != product_id:
        return jsonify({"error": "Specification not found or does not belong to this product"}), 404

    db.session.delete(specification)
    db.session.commit()

    return jsonify({"message": f"Specification '{specification.specification_name}' removed from product."}), 200
