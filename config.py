from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

# Use MongoDB Atlas Connection String
app.config["MONGO_URI"] = "mongodb+srv://<vishwajeetbhate33>:<rBt7C1bfFH89FBI9>@cluster0.mongodb.net/skillxcel?retryWrites=true&w=majority"

mongo = PyMongo(app)
