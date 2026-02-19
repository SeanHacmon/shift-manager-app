import bcrypt
import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()
mongodb_uri = os.getenv('MONGODB_URI')
client = MongoClient(mongodb_uri)
db = client['ShiftManagerApp']
users_collection = db['Bartenders']

class User:

    def __init__(self,firstName, lastName, email, password,
                 veteran, department, availableDays, role) -> None:
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = self.hash_password(password)
        self.veteran = veteran
        self.department = department
        self.availableDays = availableDays
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
            'availableDays': self.availableDays,
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
        from bson.objectid import ObjectId
        result = users_collection.delete_one({'_id': ObjectId(self._id)})
        return result.deleted_count > 0