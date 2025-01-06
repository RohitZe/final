from flask import Flask, render_template, jsonify, redirect, url_for
from pymongo import MongoClient
from bson.json_util import dumps
import os

app = Flask(__name__)

# MongoDB connection function
def connect_to_mongodb():
    """Connects to MongoDB and returns the collection."""
    try:
        CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "mongodb+srv://Rohit:Rohit1234@cluster0.lhrx5.mongodb.net/")
        client = MongoClient(CONNECTION_STRING)
        db = client["twitter_data"]
        return db["whats_happening"]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

# Fetch data from MongoDB
def get_mongodb_data():
    """Fetches data from MongoDB and returns it as a list."""
    collection = connect_to_mongodb()
    if collection is not None:  # Explicitly check if the collection is not None
        try:
            data = list(collection.find().sort("end_time", -1))  # Sort by latest end_time
            return data
        except Exception as e:
            print(f"Error fetching data from MongoDB: {e}")
            return []
    else:
        print("MongoDB collection is None.")
    return []

@app.route("/")
def home():
    """Renders the homepage with a link to run the script."""
    return render_template("home.html")

@app.route("/run_script")
def run_script():
    """Handles running the script and displays the results."""
    data = get_mongodb_data()
    if data:
        # Assuming the first document is the most relevant
        result = data[0]
        return render_template("results.html", result=result)
    else:
        return "No data available.", 404

@app.route("/api/trends", methods=["GET"])
def api_trends():
    """API endpoint to return trends data in JSON format."""
    data = get_mongodb_data()
    return jsonify(dumps(data))  # Convert BSON to JSON

if __name__ == "__main__":
    app.run(debug=True)
