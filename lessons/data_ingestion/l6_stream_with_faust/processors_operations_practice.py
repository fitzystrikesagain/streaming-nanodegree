import random
from abc import ABC
from dataclasses import dataclass

import faust

IN_TOPIC = "com.udacity.streams.clickevents"
OUT_TOPIC = "com.udacity.streams.clickevents.scored"


@dataclass
class ClickEvent(faust.Record, ABC):
    email: str
    timestamp: str
    uri: str
    number: int
    fraud_score: float = 0.0
    fraud_likely: bool = False


def add_score(click):
    fraud_score = round(random.random(), 2)
    click.fraud_score = fraud_score
    if fraud_score > .8:
        click.fraud_likely = True
    return click


app = faust.App("exercise5", broker="kafka://localhost:9092")
clickevents_topic = app.topic(IN_TOPIC, value_type=ClickEvent)
fraud_scored_topic = app.topic(
    OUT_TOPIC,
    key_type=str,
    value_type=ClickEvent,
)


@app.agent(clickevents_topic)
async def clickevent(clickevents):
    clickevents.add_processor(add_score)
    async for ce in clickevents:
        await fraud_scored_topic.send(key=ce.uri, value=ce)


if __name__ == "__main__":
    app.main()
