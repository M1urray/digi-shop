from flask import jsonify, request
from app.orders import bp
from app.model import Order, OrderItem, Product, Customer, Address
from app.extensions import db
# add cors
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError


# add cors in post order

CORS(bp)


@bp.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    
    try:
        # Create a new customer if it doesn't exist
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
        
        # Add shipping address
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

        # Create the order with correct address_id
        new_order = Order(
            customer_id=customer.id,
            address_id=address.id,  # Corrected field here
            notes=data.get('orderNotes', None)
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
        db.session.rollback()  # Roll back the transaction on error
        return jsonify({"error": str(e)}), 500  # Return the error for debugging

    except KeyError as e:
        return jsonify({"error": f"Missing key: {e}"}), 400  # Handle missing data keys

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



@bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    items = []
    for item in order.items:
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


@bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)

    OrderItem.query.filter_by(order_id=order.id).delete()
    
    db.session.delete(order)
    db.session.commit()

    return jsonify({"message": "Order deleted successfully!"}), 200
