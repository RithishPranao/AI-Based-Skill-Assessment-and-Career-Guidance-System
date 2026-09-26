import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file")

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)

# Select database
db = client["AI_Career_Guidance"]

# Collections
students_collection = db["students"]
parents_collection = db["parents"]
assessments_collection = db["assessments"]
career_results_collection = db["career_results"]
learning_resources_collection = db["learning_resources"]
progress_collection = db["progress"]


def test_connection():
    """Test MongoDB connection."""
    client.admin.command("ping")
    print("MongoDB connection successful!")


if __name__ == "__main__":
    test_connection()
