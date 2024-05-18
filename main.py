from datetime import datetime, timedelta

import pymongo

from config import USER_NAME, USER_PASS


def generate_date_range(start_date, end_date, step):
    dates = []
    current_date = start_date
    while current_date <= end_date:
        if step == "month":
            break

        dates.append(current_date.strftime("%Y-%m-%dT%H:%M:%S"))

        if step == "day":
            current_date += timedelta(days=1)
        if step == "hour":
            current_date += timedelta(hours=1)
    return dates


def payments(dt_from, dt_upto, group_type):
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

    data = {f"{item['_id']}{end}": item['total'] for item in result}
    if not group_type == "month":
        date_list = generate_date_range(dt_from, dt_upto, group_type)

        labels = []
        dataset = []
        for date in date_list:
            labels.append(date)
            dataset.append(data.get(date, 0))
    else:
        dataset = [item['total'] for item in result]
        labels = [f"{item['_id']}{end}" for item in result]

    return {"dataset": dataset, "labels": labels}
