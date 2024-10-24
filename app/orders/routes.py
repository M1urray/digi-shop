from flask import jsonify, request
from app.orders import bp
from app.model import Order, OrderItem, Product, Customer, Address
from app.extensions import db

@bp.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    
    # Create a new customer if it doesn't exist
    customer_data = data['customer']
    customer = Customer.query.filter_by(email=customer_data['email']).first()
    if not customer:
        customer = Customer(
            fname=customer_data['fname'],
            lname=customer_data['lname'],
            company_name=customer_data.get('company_name', ''),
            email=customer_data['email'],
            phone=customer_data['phone']
        )
        db.session.add(customer)
        db.session.commit()
    
    # Add shipping address
    shipping_data = customer_data['shipping_address']
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
        notes=data.get('notes', None)
    )
    db.session.add(new_order)
    db.session.commit()

    # Add order items
    for item in data['items']:
        product = Product.query.get(item['product_id'])
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        order_item = OrderItem(
            product_id=product.id,
            quantity=item['quantity'],
            order_id=new_order.id
        )
        db.session.add(order_item)

    db.session.commit()
    return jsonify({"message": "Order placed successfully!"}), 201


@bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    order_items = OrderItem.query.filter_by(order_id=order.id).all()

    items = []
    for item in order_items:
        product = Product.query.get(item.product_id)
        items.append({
            'product_name': product.name,
            'brand': product.brand.name,
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
