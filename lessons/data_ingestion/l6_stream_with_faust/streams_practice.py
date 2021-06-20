from abc import ABC
from dataclasses import asdict, dataclass
import json

import faust


@dataclass
class ClickEvent(faust.Record, ABC):
    email: str
    timestamp: str
    uri: str
    number: int


app = faust.App("exercise4", broker="kafka://localhost:9092")
clickevents_topic = app.topic("com.udacity.streams.clickevents", value_type=ClickEvent)
popular_uris_topic = app.topic(
    "com.udacity.streams.clickevents.popular",
    key_type=str,
    value_type=ClickEvent,
)


@app.agent(clickevents_topic)
async def clickevent(clickevents):
    # Filter clickevents to only those with a number higher than or equal to 100
    async for click in clickevents.filter(lambda x: x.number >= 100):
        # Send the message to the `popular_uris_topic` with a key and value.
        await popular_uris_topic.send(key=click.uri, value=click)
    pass


if __name__ == "__main__":
    app.main()
