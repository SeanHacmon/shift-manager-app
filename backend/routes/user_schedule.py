import os
from dotenv import load_dotenv
from pymongo import MongoClient

from flask import Blueprint, request, jsonify
from models.user import User

load_dotenv()

mongodb_uri = os.getenv('MONGODB_URI')
client = MongoClient(mongodb_uri)
db = client['ShiftManagerApp']


schedule_bp = Blueprint('auth', __name__)

@schedule_bp.route('/create', methods=['POST'])
def create_schedule():
    pass

@schedule_bp.route('/publish', methods=['PUT'])
def publish_schedule():
    pass

@schedule_bp.route('/', methods=['GET'])
def get_schedule():
    pass
