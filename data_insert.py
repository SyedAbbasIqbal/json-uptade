from pymongo import MongoClient, errors
from faker import Faker
import logging
import time
import os
from dotenv import load_dotenv


load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

start_time = time.time()
logging.info("Process started.")

try:
   
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI not found in .env file")

    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

    
    db = client["CustomerDetails"]
    collection = db["CustomerRecords"]

    
    client.admin.command("ping")
    logging.info("Connected to MongoDB successfully!")

   
    fake = Faker()
    batch_size = 100000  
    records = []

    for i in range(1, 1_000_001):
        customer = {
            "customer_id": i,
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address().replace('\n', ', '),
            "phone": fake.phone_number(),
            "age": fake.random_int(min=18, max=90)
        }
        records.append(customer)

        
        if i % batch_size == 0:
            collection.insert_many(records)
            logging.info(f"Inserted {i} records...")
            records = []

    
    if records:
        collection.insert_many(records)
        logging.info(f"Inserted remaining {len(records)} records.")

    
    last_10 = collection.find().sort("customer_id", -1).limit(10)
    last_10_ids = [doc["customer_id"] for doc in last_10]
    delete_result = collection.delete_many({"customer_id": {"$in": last_10_ids}})
    logging.info(f"Deleted {delete_result.deleted_count} records (last 10).")

    logging.info("Process completed successfully!")
    print("All 1 million records inserted into MongoDB Atlas and last 10 deleted.")

except errors.ConnectionFailure as e:
    logging.error(f"MongoDB connection failed: {e}")
    print(f"MongoDB connection failed: {e}")

except Exception as e:
    logging.error(f"Unexpected error: {e}")
    print(f"An unexpected error occurred: {e}")

finally:
    end_time = time.time()
    total_time = end_time - start_time
    logging.info(f"Total time taken: {total_time:.2f} seconds")
    print(f"Total time taken: {total_time:.2f} seconds")
