import json
from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv

load_dotenv() 

user = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")
db_name = os.getenv("MONGO_DB")
cluster = os.getenv("MONGO_CLUSTER")

try:
    client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}.mongodb.net/{db_name}?retryWrites=true&w=majority")
    db = client[db_name]
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

