from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from functools import wraps
from flask import request, jsonify
from app.model import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  # Get the token from the headers

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode the token here (replace `decode_token_function` with your actual decode function)
            user_data = User.verify_jwt(token)
            if not user_data:
                return jsonify({'message': 'Token is invalid!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated