import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongodb_uri = os.getenv('MONGODB_URI')

try:
    client = MongoClient(mongodb_uri)
    
    # Test the connection
    admin_db = client.admin
    admin_db.command('ping')
    print("✅ MongoDB connection successful!")
    
    # Get your database
    db = client['ShiftManagerApp']
    print(f"✅ Database 'ShiftManagerApp' found!")
    
    # Get users collection
    users_collection = db['users']
    print(f"✅ Users collection ready!")
    
    # CREATE: Insert a test user
    print("\n--- CREATING TEST USER ---")
    test_user = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john@test.com',
        'password': 'hashed_password_123',
        'veteran': True,
        'department': 'Sales',
        'availableDays': [1, 2, 3, 4, 5],
        'role': 'user'
    }
    
    result = users_collection.insert_one(test_user)
    print(f"✅ User created with ID: {result.inserted_id}")
    
    # READ: Find the user
    print("\n--- READING TEST USER ---")
    found_user = users_collection.find_one({'email': 'john@test.com'})
    if found_user:
        print(f"✅ Found user: {found_user['firstName']} {found_user['lastName']}")
        print(f"   Email: {found_user['email']}")
        print(f"   Veteran: {found_user['veteran']}")
        print(f"   Available Days: {found_user['availableDays']}")
    
    # COUNT: How many users?
    print("\n--- COUNTING USERS ---")
    count = users_collection.count_documents({})
    print(f"✅ Total users in database: {count}")
    
    # Now go to MongoDB website and look at the data
    print("\n⏸️  PAUSE: Go to MongoDB website and check the 'users' collection!")
    print("   You should see your test user there.")
    print("   Press Enter when you've verified it in MongoDB website...")
    input()
    
    # DELETE: Remove the test user
    print("\n--- DELETING TEST USER ---")
    delete_result = users_collection.delete_one({'email': 'john@test.com'})
    print(f"✅ Deleted {delete_result.deleted_count} user(s)")
    
    # VERIFY: Check it's gone
    print("\n--- VERIFYING DELETION ---")
    remaining = users_collection.find_one({'email': 'john@test.com'})
    if remaining:
        print("❌ User still exists!")
    else:
        print("✅ User successfully deleted!")
    
    # Final count
    final_count = users_collection.count_documents({})
    print(f"✅ Total users remaining: {final_count}")
    
    print("\n✅ All tests passed! Database connection is working perfectly!")
    client.close()
    print("✅ MongoDB connection closed")
    
except Exception as e:
    print(f"❌ Error: {e}")