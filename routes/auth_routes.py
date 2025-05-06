from flask import Blueprint, request, jsonify
from config import mongo, app
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
import datetime

auth = Blueprint("auth", __name__)
bcrypt = Bcrypt(app)
app.config["JWT_SECRET_KEY"] = "your_secret_key"  # Change this
jwt = JWTManager(app)

users_collection = mongo.db.users  # MongoDB Collection

# User Registration
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    existing_user = users_collection.find_one({"email": data["email"]})
    
    if existing_user:
        return jsonify({"message": "User already exists"}), 400
    
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    users_collection.insert_one({
        "name": data["name"],
        "email": data["email"],
        "password": hashed_password
    })
    
    return jsonify({"message": "User registered successfully"}), 201

# User Login
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users_collection.find_one({"email": data["email"]})
    
    if user and bcrypt.check_password_hash(user["password"], data["password"]):
        access_token = create_access_token(identity=user["email"], expires_delta=datetime.timedelta(days=1))
        return jsonify({"token": access_token}), 200
    return jsonify({"message": "Invalid credentials"}), 401
