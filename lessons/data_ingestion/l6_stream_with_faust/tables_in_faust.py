from abc import ABC
from dataclasses import dataclass

import faust


@dataclass
class ClickEvent(faust.Record, ABC):
    email: str
    timestamp: str
    uri: str
    number: int


app = faust.App("exercise6", broker="kafka://localhost:9092")
clickevents_topic = app.topic("com.udacity.streams.clickevents", value_type=ClickEvent)

uri_summary_table = app.Table("uri-summary", default=int)


@app.agent(clickevents_topic)
async def clickevent(clickevents):
    async for ce in clickevents.group_by(ClickEvent.uri):
        uri_summary_table[ce.uri] += ce.number
        print(f"{ce.uri}: {uri_summary_table[ce.number]}")


if __name__ == "__main__":
    app.main()
