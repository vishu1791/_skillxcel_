from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from app import mongo  # Import the database connection

bcrypt = Bcrypt()

# Find users with plain text passwords
users = mongo.db.Users.find()
for user in users:
    if not user["password"].startswith("$2b$"):  # Check if password is already hashed
        hashed_password = bcrypt.generate_password_hash(user["password"]).decode('utf-8')
        mongo.db.Users.update_one({"_id": user["_id"]}, {"$set": {"password": hashed_password}})
        print(f"Updated password for user: {user['username']}")

print("Password update complete!")
