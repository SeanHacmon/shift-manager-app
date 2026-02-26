import os
from dotenv import load_dotenv
from pymongo import MongoClient

from flask import Blueprint, request, jsonify
from models.user import User

load_dotenv()

mongodb_uri = os.getenv('MONGODB_URI')
client = MongoClient(mongodb_uri)
db = client['ShiftManagerApp']


shifts_bp = Blueprint('auth', __name__)

@shifts_bp.route('/submit', methods=['POST'])
def submit():
    pass

@shifts_bp.route('/user/availability', methods=['GET'])
def get_user_availability():
    pass

@shifts_bp.route('/availability', methods=['GET'])
def get_all_availability():
    pass

@shifts_bp.route('/user/shifts', methods=['GET'])
def get_user_shifts():
    pass

