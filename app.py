from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv

load_dotenv()  

app = Flask(__name__)

try:
    user = os.getenv("MONGO_USER")
    password = os.getenv("MONGO_PASS")
    db_name = os.getenv("MONGO_DB")
    cluster = os.getenv("MONGO_CLUSTER")

    client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}.mongodb.net/{db_name}?retryWrites=true&w=majority&appName=Cluster0")
    db = client[db_name]
    collection = db["donuts"]   
except errors.ConnectionFailure as e:
    print(f"MongoDB connection failed: {e}")
    collection = None


@app.route("/api/donuts", methods=["GET"])
def get_donuts():
    try:
        donuts = list(collection.find({}, {"_id": 0}))
        return jsonify(donuts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/donuts", methods=["POST"])
def add_donut():
    try:
        data = request.json
        collection.insert_one(data)
        return jsonify({"msg": "Donut added!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/donuts/<name>", methods=["PUT"])
def update_donut(name):
    try:
        data = request.json
        result = collection.update_one({"name": name}, {"$set": data})
        if result.matched_count:
            return jsonify({"msg": f"{name} updated!"}), 200
        else:
            return jsonify({"error": "Donut not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/donuts/<name>", methods=["DELETE"])
def delete_donut(name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            return jsonify({"msg": f"{name} deleted!"}), 200
        else:
            return jsonify({"error": "Donut not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
