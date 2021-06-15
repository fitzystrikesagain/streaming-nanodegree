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


@dataclass
class PurchaseDollars(faust.Record, ABC):
    username: str
    currency: str
    amount: float


app = faust.App(
    "exercise2",
    broker=BROKER_URL)

purchases_topic = app.topic(
    TOPIC_NAME,
    key_type=str,
    value_type=Purchase
)
dollars_topic = app.topic(
    f"{TOPIC_NAME}.dollars",
    key_type=str,
    value_type=PurchaseDollars
)


@app.agent(purchases_topic)
async def purchase(purchases):
    async for p in purchases:
        purchase_in_dollars = PurchaseDollars(
            username=p.username,
            currency=p.currency,
            amount=p.amount / 100.0
        )
        await dollars_topic.send(key=p.username, value=purchase_in_dollars)


if __name__ == "__main__":
    app.main()
