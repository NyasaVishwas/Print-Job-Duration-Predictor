
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

MONGO_URI = "mongodb://localhost:27017/"

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

try:
    client.admin.command("ping")
    print("MongoDB connection successful!")

    db = client["printpulse"]

    print_jobs = db["print_jobs"]
    printers = db["printers"]
    prediction_history = db["prediction_history"]

except ConnectionFailure as error:
    print("MongoDB connection failed:", error)
    raise
