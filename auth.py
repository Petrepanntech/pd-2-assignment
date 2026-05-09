import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)

def create_jwt_token(user_id, email):
    payload = {
        'user_id': user_id,
        'email': email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid authorization header'}), 401

        if not token:
            return jsonify({'error': 'Authorization token missing'}), 401

        payload = decode_jwt_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401

        request.user_id = payload['user_id']
        request.user_email = payload['email']
        return f(*args, **kwargs)

    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from models import User

        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid authorization header'}), 401

        if not token:
            return jsonify({'error': 'Authorization token missing'}), 401

        payload = decode_jwt_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401

        user = User.query.get(payload['user_id'])
        if not user or not user.is_instructor:
            return jsonify({'error': 'Admin access required'}), 403

        request.user_id = payload['user_id']
        request.user_email = payload['email']
        return f(*args, **kwargs)

    return decorated