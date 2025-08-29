import json
from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv

load_dotenv() 

try:
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client["donutsdb"]
    collection = db["donuts"]

    with open("E:/Skill Rank/task/eg5.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)

    print("Data inserted into MongoDB!")

except FileNotFoundError:
    print("Error: JSON file not found.")

except json.JSONDecodeError:
    print("Error: Invalid JSON format.")

except errors.ConnectionFailure as e:
    print(f"MongoDB connection failed: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
