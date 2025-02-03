from flask import jsonify, request
from app.orders import bp
from app.model import Order, OrderItem, Product, Customer, Address
from app.extensions import db
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

CORS(bp)

# Place a new order
@bp.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    try:
        # Retrieve or create the customer
        customer_data = data['customer']
        customer = Customer.query.filter_by(email=customer_data['email']).first()
        if not customer:
            customer = Customer(
                fname=customer_data['firstName'],
                lname=customer_data['lastName'],
                company_name=customer_data.get('companyName', ''),
                email=customer_data['email'],
                phone=customer_data['phone']
            )
            db.session.add(customer)
            db.session.commit()
        
        # Create the shipping address
        shipping_data = data['shipping_address']
        address = Address(
            street=shipping_data['street'],
            town=shipping_data['town'],
            postal_code=shipping_data['postal_code'],
            country=shipping_data['country'],
            customer_id=customer.id
        )
        db.session.add(address)
        db.session.commit()

        # Create the order
        new_order = Order(
            customer_id=customer.id,
            address_id=address.id,
            notes=data.get('orderNotes')
        )
        db.session.add(new_order)
        db.session.commit()

        # Add order items
        for item in data['items']:
            product = Product.query.get(item['id'])
            if not product:
                return jsonify({"error": f"Product with ID {item['id']} not found"}), 404
            
            order_item = OrderItem(
                product_id=product.id,
                quantity=item['quantity'],
                order_id=new_order.id
            )
            db.session.add(order_item)

        db.session.commit()
        return jsonify({"message": "Order placed successfully!"}), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    except KeyError as e:
        return jsonify({"error": f"Missing key: {e}"}), 400
    
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# Retrieve an order by ID
@bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.options(joinedload(Order.customer), joinedload(Order.address), joinedload(Order.items).joinedload(OrderItem.product)).get_or_404(order_id)

    items = []
    for item in order.items:
        product = item.product
        items.append({
            'product_name': product.name,
            'brand': product.brand.name if product.brand else None,
            'quantity': item.quantity,
            'price': product.price
        })

    return jsonify({
        'order_id': order.id,
        'customer': {
            'fname': order.customer.fname,
            'lname': order.customer.lname,
            'email': order.customer.email,
            'phone': order.customer.phone
        },
        'address': {
            'street': order.address.street,
            'town': order.address.town,
            'postal_code': order.address.postal_code,
            'country': order.address.country
        },
        'items': items,
        'notes': order.notes
    })


# Retrieve all orders for a specific customer
@bp.route('/customers/<int:customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    orders = Order.query.filter_by(customer_id=customer.id).options(joinedload(Order.items).joinedload(OrderItem.product)).all()

    order_list = []
    for order in orders:
        items = []
        for item in order.items:
            product = item.product
            items.append({
                'product_name': product.name,
                'brand': product.brand.name if product.brand else None,
                'quantity': item.quantity,
                'price': product.price
            })

        order_list.append({
            'order_id': order.id,
            'address': {
                'street': order.address.street,
                'town': order.address.town,
                'postal_code': order.address.postal_code,
                'country': order.address.country
            },
            'items': items,
            'notes': order.notes
        })

    return jsonify({
        'customer': {
            'fname': customer.fname,
            'lname': customer.lname,
            'email': customer.email,
            'phone': customer.phone
        },
        'orders': order_list
    }), 200


# Retrieve all orders
# Retrieve all orders
@bp.route('/orders', methods=['GET'])
def get_all_orders():
    orders = Order.query.options(
        joinedload(Order.customer),
        joinedload(Order.address),
        joinedload(Order.items).joinedload(OrderItem.product)  # Load related product data
    ).all()

    all_orders = []
    for order in orders:
        items = []
        for item in order.items:
            product = item.product  # Access the related Product model
            items.append({
                'product_name': product.name,
                'brand': product.brand.name if product.brand else None,
                'quantity': item.quantity,
                'price': product.price
            })
        
        all_orders.append({
            'order_id': order.id,
            'customer': {
                'fname': order.customer.fname,
                'lname': order.customer.lname,
                'email': order.customer.email,
                'phone': order.customer.phone
            },
            'address': {
                'street': order.address.street,
                'town': order.address.town,
                'postal_code': order.address.postal_code,
                'country': order.address.country
            },
            'items': items,
            'notes': order.notes,
            'is_fulfilled': order.is_fulfilled,
            'total_price': sum([item['price'] * item['quantity'] for item in items])
        })
    
    return jsonify(all_orders), 200



# Delete an order by ID
@bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    OrderItem.query.filter_by(order_id=order.id).delete()
    db.session.delete(order)
    db.session.commit()

    return jsonify({"message": "Order deleted successfully!"}), 200

# @bp.route('/orders/<int:order_id>/fulfill', methods=['PUT'])
# def fulfill_order(order_id):
#     order = Order.query.get(order_id)
#     if not order:
#         return jsonify({'error': 'Order not found'}), 404
    
#     # Check if the order is already fulfilled
#     if order.is_fulfilled:
#         return jsonify({'message': 'Order already fulfilled'}), 400

#     # Ensure stock is sufficient for each item
#     for item in order.items:
#         product = Product.query.get(item.product_id)
#         if product.stock < item.quantity:
#             return jsonify({
#                 'error': f'Insufficient stock for product {product.name} (id: {product.id})'
#             }), 400
    
#     # Deduct stock and mark order as fulfilled
#     for item in order.items:
#         product = Product.query.get(item.product_id)
#         product.stock -= item.quantity
#         db.session.add(product)

#     # Mark the order as fulfilled
#     order.is_fulfilled = True
#     db.session.add(order)
#     db.session.commit()

#     return jsonify({'message': 'Order fulfilled and stock updated'}), 200

@bp.route('/customers/count', methods=['GET'])
def get_customer_count():
    customer_count = Customer.query.count()
    return jsonify({'customer_count': customer_count}), 200

@bp.route('/revenue', methods=['GET'])
def get_realized_revenue():
    fulfilled_orders = Order.query.filter_by(is_fulfilled=True).all()
    total_revenue = 0

    for order in fulfilled_orders:
        for item in order.items:
            product = Product.query.get(item.product_id)
            total_revenue += product.price * item.quantity

    return jsonify({'total_revenue': total_revenue}), 200

# get all fulfilled orders
@bp.route('/orders/fulfilled', methods=['GET'])
def get_fulfilled_orders():
    orders = Order.query.filter_by(is_fulfilled=True).options(
        joinedload(Order.customer),
        joinedload(Order.address),
        joinedload(Order.items).joinedload(OrderItem.product)
    ).all()

    all_orders = []
    for order in orders:
        items = []
        for item in order.items:
            product = item.product
            items.append({
                'product_name': product.name,
                'brand': product.brand.name if product.brand else None,
                'quantity': item.quantity,
                'price': product.price
            })
        
        all_orders.append({
            'order_id': order.id,
            'customer': {
                'fname': order.customer.fname,
                'lname': order.customer.lname,
                'email': order.customer.email,
                'phone': order.customer.phone
            },
            'address': {
                'street': order.address.street,
                'town': order.address.town,
                'postal_code': order.address.postal_code,
                'country': order.address.country
            },
            'items': items,
            'notes': order.notes,
            'is_fulfilled': order.is_fulfilled
        })
    
    return jsonify(all_orders), 200

# update order from unfulfilled to fulfilled
@bp.route('/orders/<int:order_id>/fulfill', methods=['PUT'])
def fulfill_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Check if the order is already fulfilled
    if order.is_fulfilled:
        return jsonify({'message': 'Order already fulfilled'}), 400

    # Ensure stock is sufficient for each item
    for item in order.items:
        product = Product.query.get(item.product_id)
        if product.stock < item.quantity:
            return jsonify({
                'error': f'Insufficient stock for product {product.name} (id: {product.id})'
            }), 400
    
    # Deduct stock and mark order as fulfilled
    for item in order.items:
        product = Product.query.get(item.product_id)
        product.stock -= item.quantity
        db.session.add(product)

    # Mark the order as fulfilled
    order.is_fulfilled = True
    db.session.add(order)
    db.session.commit()

    return jsonify({'message': 'Order fulfilled and stock updated'}), 200
