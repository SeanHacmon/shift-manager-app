import bcrypt
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

load_dotenv()
mongodb_uri = os.getenv('MONGODB_URI')
client = MongoClient(mongodb_uri)
db = client['ShiftManagerApp']
users_collection = db['Bartenders']

class User:

    def __init__(self,firstName, lastName, email, password,
                 veteran, department, availability, role) -> None:
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = self.hash_password(password)
        self.veteran = veteran
        self.department = department
        self.availability = availability
        self.role = role

    def hash_password(self, password:str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def compare_password(self, otherPassword:str) -> bool:
        return bcrypt.checkpw(otherPassword.encode('utf-8'), 
                             self.password.encode('utf-8'))
    
    def saveUserInDB(self):
        user_data = {
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'password': self.password,
            'veteran': self.veteran,
            'department': self.department,
            'availability': self.availability,
            'shifts': [],
            'role': self.role
        }
        result = users_collection.insert_one(user_data)
        self._id = result.inserted_id 
        return result.inserted_id

    @staticmethod
    def findUserByEmail(email:str):
        return users_collection.find_one({'email': email})


    @staticmethod
    def delete_from_db(self):
        """Delete this user from database using self._id"""
        result = users_collection.delete_one({'_id': ObjectId(self._id)})
        return result.deleted_count > 0
    
    @staticmethod
    def update_availability(user_id: str, availability: list):
        result = users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'availability': availability}}
        )
        return result.modified_count > 0
    
    @staticmethod
    def get_availability(user_id):
        user = users_collection.find_one(
            {'_id': ObjectId(user_id)},
            {'availableDays': 1}  # only fetch this field
        )
        return user['availableDays'] if user else None
    
    @staticmethod
    def get_all_availability():
        users = users_collection.find({}, {'firstName': 1, 'availableDays': 1})
        return {user['firstName']: user['availableDays'] for user in users}
    

    @staticmethod
    def get_shifts(user_id):
        user = users_collection.find_one(
            {'_id': ObjectId(user_id)},
            {'shifts': 1}
        )
        return user['shifts'] if user else None

    @staticmethod
    def update_shifts(user_id, shifts):
        result = users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'shifts': shifts}}
        )
        return result.modified_count > 0