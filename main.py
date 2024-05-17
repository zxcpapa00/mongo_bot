import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

USER_NAME = os.getenv("USER_NAME")
USER_PASS = os.getenv("USER_PASS")

client = (
    pymongo.mongo_client.MongoClient(
        f"mongodb+srv://{USER_NAME}:{USER_PASS}@cluster0.gmpmurs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
)
collection = client['sampleDB'].get_collection('sample_collection')
