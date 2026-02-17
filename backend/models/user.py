import pymongo
import bcrypt
import datetime


client = MongoClient('mongodb://localhost:27017/')
db = client['shift-manager']
users_collection = db['users']

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
        return result.inserted_id

    @staticmethod
    def findUserByEmail(email:str):
        return users_collection.find_one({'email': email})

