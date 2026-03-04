import os
from dotenv import load_dotenv
from pymongo import MongoClient
from flask import Blueprint, request, jsonify
from validation.shift_validation import *
from validation.user_validation import *
from models.user import *
from middleware.jwt import *

load_dotenv()

mongodb_uri = os.getenv('MONGODB_URI')
client = MongoClient(mongodb_uri)
db = client['ShiftManagerApp']


shifts_bp = Blueprint('shifts', __name__)

@shifts_bp.route('/submit', methods=['POST'])
@auth_middleware
def submit():
    data = request.get_json()
    user_id = request.user_id
    user, msg = validate_user_exists_by_id(user_id)
    if not user:
        return jsonify({'message': msg}, 400)
    valid, msg = validate_availability(data['availability'])
    if not valid:
        return jsonify({'message': msg}, 400)
    
    User.update_availability(user_id, data['availability'])
    return jsonify({'message':'Shifts have been submited successfuly'}, 200)
    
@shifts_bp.route('/user/availability', methods=['GET'])
@auth_middleware
def get_user_availability():
    availability = User.get_availability(request.user_id)
    if availability is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'availability': availability}), 200

@shifts_bp.route('/user/availability/<user_id>', methods=['GET'])
@auth_middleware
def get_user_availability_by_id(user_id):
    if request.role != 'manager':
        return jsonify({'message': 'Unauthorized'}), 403
    
    availability = User.get_availability(user_id)
    if availability is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'availability': availability}), 200

@shifts_bp.route('/availability', methods=['GET'])
@auth_middleware
def get_all_availability():
    if request.role != 'manager':
        return jsonify({'message': 'Unauthorized'}), 403
    
    availability = User.get_all_availability()
    return jsonify({'availability': availability}), 200

@shifts_bp.route('/user/shifts', methods=['GET'])
@auth_middleware
def get_user_shifts():
    shifts = User.get_shifts(request.user_id)
    if shifts is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'shifts': shifts}), 200

