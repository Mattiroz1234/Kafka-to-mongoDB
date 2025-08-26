from fastapi import FastAPI
from loader import get_interesting, get_not_interesting
from kafka import KafkaProducer
import json
import uvicorn

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

interesting_msgs = get_interesting()
not_interesting_msgs = get_not_interesting()

@app.get("/publish_20_newsgroups")
def publish_20_newsgroups():
    for x, y in interesting_msgs.items():
        if len(y) > 0:
            msg = {'subject': x, 'text': y.pop()}
            producer.send('interesting', {'message': msg})

    for x, y in not_interesting_msgs.items():
        if len(y) > 0:
            msg = {'subject': x, 'text': y.pop()}
            producer.send('not_interesting', {'message': msg})

    producer.flush()
    return {"status": "published", "count": 20}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

