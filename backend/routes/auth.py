import os
from dotenv import load_dotenv
from pymongo import MongoClient
from validation.user_validation import *
from flask import Blueprint, request, jsonify
from models.user import User

load_dotenv()

mongodb_uri = os.getenv('MONGODB_URI')
client = MongoClient(mongodb_uri)
db = client['ShiftManagerApp']


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    exist, error = validate_user_not_exists(data['email'])
    if not exist:
        return jsonify({'error': error}), 409


    valid, error = validate_registration_fields(data)
    if not valid:
        return jsonify({'error': error}), 400

    user = User(data['firstName'], data['lastName'], data['email'], data['password'],
                data['veteran'], data['department'], data['availability'],data['role'])
    user.saveUserInDB()
    return jsonify({'message': 'User created successfully'}), 201

    


@auth_bp.route('/login', methods=['POST'])
def login():
    pass


@auth_bp.route('/user', methods=['GET'])
def getUser():
    pass