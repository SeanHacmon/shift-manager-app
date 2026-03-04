import jwt
from flask import request, jsonify
from functools import wraps
import os

def auth_middleware(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  # "Bearer <token>"
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        try:
            token = token.split(' ')[1]  # remove "Bearer " prefix
            decoded = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
            request.user_id = decoded['user_id']  # attach user_id to request
            request.role = decoded['role']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated