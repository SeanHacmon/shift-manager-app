import os
from dotenv import load_dotenv
from pymongo import MongoClient
from validation.user_validation import *
from flask import Blueprint, request, jsonify
from models.user import *

# load_dotenv()

# mongodb_uri = os.getenv('MONGODB_URI')
# client = MongoClient(mongodb_uri)
# db = client['ShiftManagerApp']


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    valid, error = validate_registration_fields(data)
    if not valid:
        return jsonify({'error': error}), 400

    exists, error = validate_user_not_exists(data['email'])
    if not exists:
        return jsonify({'error': error}), 409

    user = User(data['firstName'], data['lastName'], data['email'], data['password'],
                data['veteran'], data['department'], data['availability'],data['role'])
    
    user.saveUserInDB()
    return jsonify({'message': 'User created successfully'}), 201

    


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    valid, error = validate_login_fields(data)
    if not valid:
        return jsonify({'message': error}), 400
    
    user, error = validate_user_exists_by_email(data['email'])
    if not user:
        return jsonify({'message': error}), 404

    is_match, error = validate_password(data['password'], user['password'])
    if not is_match:
        return jsonify({'error': error}), 401

    return jsonify({'message': 'User logged in successfully'}), 200


@auth_bp.route('/user', methods=['GET'])
def getUser():
    pass