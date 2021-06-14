from abc import ABC
from dataclasses import asdict, dataclass
import json

import faust

BROKER_URL = "kafka://localhost:9092"
TOPIC_NAME = "com.udacity.streams.purchases"


@dataclass
class Purchase(faust.Record, ABC):
    username: str
    currency: str
    amount: int


app = faust.App(
    "exercise2",
    broker=BROKER_URL)

purchases_topic = app.topic(
    TOPIC_NAME,
    key_type=str,
    value_type=Purchase
)


@app.agent(purchases_topic)
async def purchase(purchases):
    async for p in purchases:
        print(json.dumps(asdict(p), indent=2))


if __name__ == "__main__":
    app.main()
