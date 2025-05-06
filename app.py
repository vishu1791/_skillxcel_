from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from flask_cors import CORS
from pymongo import MongoClient
import datetime
import os
import torch
import requests
import json
import re
import google.generativeai as genai

from transformers import AutoModelForCausalLM, AutoTokenizer


# Initialize Flask app
app = Flask(__name__, template_folder=os.path.abspath("templates"), static_folder="static")
CORS(app)


# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/SkillXcel"
mongo = PyMongo(app)

# Secret Key for JWT Authentication
app.config["JWT_SECRET_KEY"] = "your_secret_key_here"
jwt = JWTManager(app)

bcrypt = Bcrypt(app)
users_collection = mongo.db.Users  # MongoDB Users Collection



@app.route('/')
def login_page():
    return render_template('login.html')  # Login Page
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mobile = request.form['mobile']
        skilllevel = request.form['skilllevel']
        education_level = request.form['education_level']
        existing_user = users_collection.find_one({"username": username})
        
        if existing_user:
            return jsonify({"message": "Username already exists"}), 400
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users_collection.insert_one({
            "username": username,
            "mobile": mobile,
            "password": hashed_password,
            "skilllevel": skilllevel,
            "education_level": education_level
        })
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.get_json()
    existing_user = users_collection.find_one({"username": data["username"]})
    
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400
    
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    users_collection.insert_one({
        "username": data["username"],
        "mobile": data["mobile"],
        "password": hashed_password,
        "skilllevel": data["skilllevel"],
        "education_level": data["education_level"]
    })
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users_collection.find_one({"username": data["username"]})
    
    if user and bcrypt.check_password_hash(user["password"], data["password"]):
        access_token = create_access_token(identity=user["username"], expires_delta=datetime.timedelta(days=1))
        return jsonify({"token": access_token, "username": user["username"], "message": "Login successful!"}), 200
    
    return jsonify({"message": "Invalid credentials"}), 401

# Protected Homepage Route
@app.route('/home')
def homepage():
    username = request.cookies.get('username')  # Retrieve the cookie
    if username:
        return render_template('homepage.html', username=username)
    return redirect(url_for('login_page'))

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/courses')
def courses():
    return render_template('courses.html')
@app.route("/quiz")
def quiz():
    return render_template("javaquiz.html")
@app.route("/network")
def network():
    return render_template("networkquiz.html") 
@app.route("/web")
def web():
    return render_template("webquiz.html") 
@app.route("/python")
def python():
    return render_template("pythonQuiz.html") 
@app.route("/roadmap")
def roadmap():
    return render_template("roadmap.html") 
@app.route("/beg_java")
def beg_java():
    return render_template("beg_java.html")
@app.route("/int_java")
def int_java():
    return render_template("int_java.html")
@app.route("/adv_java")
def adv_java():
    return render_template("adv_java.html")
@app.route("/beg_python")
def beg_python():
    return render_template("beg_python.html")
@app.route("/int_python")
def int_python():
    return render_template("int_python.html")
@app.route("/adv_python")
def adv_python():
    return render_template("adv_python.html")
@app.route("/beg_web")
def beg_web():
    return render_template("beg_web.html")
@app.route("/int_web")
def int_web():
    return render_template("int_web.html")
@app.route("/adv_web")
def adv_web():
    return render_template("adv_web.html")
# Chatbot functionality




@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


if __name__ == "__main__":
    app.run(debug=True)
