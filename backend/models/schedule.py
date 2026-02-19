from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
mongodb_uri = os.getenv('MONGODB_URI')
client = MongoClient(mongodb_uri)
db = client['ShiftManagerApp']
users_collection = db['users']

class Schedule:
    def __init__(self, schedule_dict, manager_id):
        self.schedule = schedule_dict  # {"Niv": [1,2,4], "John": [3,5,6]}
        self.isPublished = False
        self.manager_id = manager_id  # The manager who created it
    
    def save_to_db(self):
        """Save schedule to the manager's document"""
        schedule_data = {
            'schedule': self.schedule,
            'isPublished': self.isPublished
        }
        
        # Update manager's document with schedule
        result = users_collection.update_one(
            {'_id': self.manager_id, 'role': 'manager'},
            {'$set': schedule_data}
        )
        
        return result.modified_count > 0
    
    def publish(self):
        """Publish the schedule"""
        result = users_collection.update_one(
            {'_id': self.manager_id},
            {'$set': {'isPublished': True}}
        )
        return result.modified_count > 0
    
    @staticmethod
    def get_current_schedule():
        """Get current published schedule from any manager"""
        return users_collection.find_one(
            {'role': 'manager', 'isPublished': True},
            sort=[('_id', -1)]
        )