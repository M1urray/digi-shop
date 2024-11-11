from flask import jsonify
from app.hotdeals import bp
from app.model import Product

@bp.route('/hot-deals', methods=['GET'])
def get_hot_deals():
    try:
        # Query products marked as hot deals and eager load their associated brand data
        hot_deals = Product.query.filter_by(is_hot_deal=True).all()
        
        # Build the response data
        result = []
        for deal in hot_deals:
            result.append({
                "id": deal.id,
                "name": deal.name,
                "price": deal.price,
                "rating": deal.rating,
                "discount": deal.discount,
                "image": deal.image,
                "brand": deal.brand.name if deal.brand else None,  # Include brand name if available,
                "category": deal.category.name,
                "subcategory": deal.subcategory.name
            })
        
        return jsonify({"products": result}), 200
    except Exception as e:
        return jsonify({"message": "Failed to retrieve hot deals", "error": str(e)}), 500
