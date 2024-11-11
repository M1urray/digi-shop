from flask import Blueprint, render_template, request, jsonify, current_app
from app.model import User
from app.extensions import db, token_required
from app.users import bp
# add corse
from flask_cors import CORS


CORS(bp);
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({'error': 'User already exists'}), 400
    
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = user.generate_jwt()
    username = user.username
    userId = user.id
    return jsonify({'token': token, 'user': username,'userid': userId}), 200


# enable cors
CORS(bp);
@bp.route('/change-password', methods=['POST'])
@token_required
def change_password():
    data = request.get_json()
    user_id = data.get('userId')
    currentPassword = data.get('currentPassword')
    newPassword = data.get('newPassword')

    if not currentPassword or not newPassword:
        return jsonify({'error': 'Old password and new password are required'}), 400

    user = User.query.get(user_id)

    if user is None or not user.check_password(currentPassword):
        return jsonify({'error': 'Invalid old password'}), 401

    user.set_password(newPassword)
    db.session.commit()

    return jsonify({'message': 'Password updated successfully'}), 200
