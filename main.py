from datetime import datetime

import pymongo
from dotenv import load_dotenv
import os

load_dotenv()


def payments(dt_from, dt_upto, group_type):
    USER_NAME = os.getenv("USER_NAME")
    USER_PASS = os.getenv("USER_PASS")

    client = (
        pymongo.mongo_client.MongoClient(
            f"mongodb+srv://{USER_NAME}:{USER_PASS}@cluster0.gmpmurs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        )
    )
    collection = client['sampleDB'].get_collection('sample_collection')
    dt_from = datetime.fromisoformat(dt_from)
    dt_upto = datetime.fromisoformat(dt_upto)

    if group_type == "month":
        end = "-01T00:00:00"
        date_format = "%Y-%m"
    elif group_type == "day":
        end = "T00:00:00"
        date_format = "%Y-%m-%d"
    elif group_type == "hour":
        end = ":00:00"
        date_format = "%Y-%m-%dT%H"
    else:
        return {"dataset": [], "labels": []}

    pipeline = [
        {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
        {"$group": {"_id": {"$dateToString": {"format": date_format, "date": "$dt"}},
                    "total": {"$sum": "$value"}}
         },
        {
            "$sort": {"_id": 1}
        }
    ]

    result = list(collection.aggregate(pipeline))

    dataset = [item['total'] for item in result]
    labels = [f"{item['_id']}{end}" for item in result]

    return {"dataset": dataset, "labels": labels}
