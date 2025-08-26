from fastapi import FastAPI
from kafka import KafkaConsumer
from pymongo import MongoClient
from datetime import datetime
import json
import threading
import uvicorn
from contextlib import asynccontextmanager


client = MongoClient("mongodb://localhost:27017")
db = client["newsgroups_db"]
collection = db["interesting"]

consumer = KafkaConsumer(
    'interesting',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='sub_group_1',
    auto_offset_reset = 'earliest'
)

def consume_messages():
    for msg in consumer:
        collection.insert_one({
            "message": msg.value["message"],
            "timestamp": str(datetime.now())
        })


@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=consume_messages, daemon=True)
    thread.start()
    yield

    consumer.close()
    client.close()


app = FastAPI(lifespan=lifespan)


@app.get("/data")
def get_interesting_data():
    return list(collection.find({}, {"_id": 0}))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
