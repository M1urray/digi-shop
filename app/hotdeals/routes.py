from flask import jsonify
from app.hotdeals import bp
from app.model import Product

@bp.route('/hot-deals/', methods=['GET'])
def get_hot_deals():
    hot_deals = Product.query.filter_by(is_hot_deal=True).all()
    result = []
    for deal in hot_deals:
        result.append({
            "id": deal.id,
            "name": deal.name,
            "price": deal.price,
            "rating": deal.rating,
            "discount": deal.discount,
            "image": deal.image,
            "brand": deal.brand.name
        })
    return jsonify({"products": result})
