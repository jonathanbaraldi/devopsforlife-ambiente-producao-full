from flask import Flask, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os


app = Flask(__name__)

# Connect to the MongoDB instance running in your Kubernetes cluster
mongodb_username = os.environ["MONGODB_USERNAME"]
mongodb_password = os.environ["MONGODB_PASSWORD"]

client = MongoClient(f"mongodb://{mongodb_username}:{mongodb_password}@mongodb-service.default.svc.cluster.local:27017/")

db = client["devops_db"]
counter = db["counter"]

@app.route('/devops', methods=['GET'])
def get_counter():
    counter_id = ObjectId("60d5ec9a6d1e8e3dd9a3a47d")
    counter_doc = counter.find_one({"_id": counter_id})
    
    if counter_doc is None:
        counter.insert_one({"_id": counter_id, "count": 1})
        current_count = 1
    else:
        current_count = counter_doc["count"]
        counter.update_one({"_id": counter_id}, {"$set": {"count": current_count + 1}})
    
    return jsonify({"count": current_count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
