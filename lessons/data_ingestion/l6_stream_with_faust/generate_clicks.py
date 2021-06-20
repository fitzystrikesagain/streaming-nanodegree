import logging
from dataclasses import asdict, dataclass, field
import json
import time
import random

from confluent_kafka import Producer
from faker import Faker

from lessons.data_ingestion.utils.constants import BROKER_URL

faker = Faker()
CLICKS_TOPIC = "com.udacity.streams.clickevents"
PAGES_TOPIC = "com.udacity.streams.pages"


@dataclass
class Page:
    uri: str = field(default_factory=faker.uri)
    description: str = field(default_factory=faker.uri)
    created: str = field(default_factory=faker.iso8601)


@dataclass
class ClickEvent:
    email: str = field(default_factory=faker.email)
    timestamp: str = field(default_factory=faker.iso8601)
    uri: str = field(default_factory=faker.uri)
    number: int = field(default_factory=lambda: random.randint(0, 999))


def produce():
    """Produces data into the Kafka Topic"""
    p = Producer({"bootstrap.servers": BROKER_URL})

    pages = [Page() for _ in range(500)]
    for page in pages:
        p.produce(
            PAGES_TOPIC,
            value=json.dumps(asdict(page)),
            key=page.uri,
        )

    # Now start simulating clickevents for the pages
    while True:
        page = random.choice(pages)
        click = ClickEvent(uri=page.uri)
        p.produce(
            CLICKS_TOPIC,
            value=json.dumps(asdict(click)),
            key=click.uri,
        )
        time.sleep(0.1)


def main():
    """Checks for topic and creates the topic if it does not exist"""
    try:
        produce()
    except KeyboardInterrupt as e:
        logging.error(e)
        print("shutting down")


if __name__ == "__main__":
    main()
