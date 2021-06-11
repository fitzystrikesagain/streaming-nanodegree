import asyncio
from dataclasses import asdict, dataclass, field
import random

from confluent_kafka.avro import AvroConsumer, AvroProducer, CachedSchemaRegistryClient, loads
from faker import Faker

faker = Faker()

SCHEMA_REGISTRY_URL = "http://localhost:8081"
BROKER_URL = "PLAINTEXT://localhost:9092"


@dataclass
class ClickAttribute:
    element: str = field(default_factory=lambda: random.choice(["div", "a", "button"]))
    content: str = field(default_factory=faker.bs)

    @classmethod
    def attributes(self):
        return {faker.uri_page(): ClickAttribute() for _ in range(random.randint(1, 5))}


@dataclass
class ClickEvent:
    email: str = field(default_factory=faker.email)
    timestamp: str = field(default_factory=faker.iso8601)
    uri: str = field(default_factory=faker.uri)
    number: int = field(default_factory=lambda: random.randint(0, 999))
    attributes: dict = field(default_factory=ClickAttribute.attributes)

    schema = loads("""{
        "type": "record",
        "name": "click_event",
        "namespace": "com.udacity.lesson3.exercise4",
        "fields": [
            {"name": "email", "type": "string"},
            {"name": "timestamp", "type": "string"},
            {"name": "uri", "type": "string"},
            {"name": "number", "type": "int"},
            {
                "name": "attributes",
                "type": {
                    "type": "map",
                    "values": {
                        "type": "record",
                        "name": "attribute",
                        "fields": [
                            {"name": "element", "type": "string"},
                            {"name": "content", "type": "string"}
                        ]
                    }
                }
            }
        ]
    }""")


async def produce(topic_name):
    """Produces data into the Kafka Topic"""
    schema_registry = CachedSchemaRegistryClient({"url": SCHEMA_REGISTRY_URL})

    p = AvroProducer(
        {"bootstrap.servers": BROKER_URL},
        schema_registry=schema_registry,
    )
    while True:
        p.produce(
            topic=topic_name,
            value=asdict(ClickEvent()),
            value_schema=ClickEvent.schema
        )
        await asyncio.sleep(1.0)


async def consume(topic_name):
    """Consumes data from the Kafka Topic"""
    schema_registry = CachedSchemaRegistryClient({"url": SCHEMA_REGISTRY_URL})

    c = AvroConsumer({
        "bootstrap.servers": BROKER_URL,
        "group.id": "0"},
        schema_registry=schema_registry,
    )
    c.subscribe([topic_name])
    while True:
        message = c.poll(1.0)
        if message is None:
            print("no message received by consumer")
        elif message.error() is not None:
            print(f"error from consumer {message.error()}")
        else:
            try:
                print(message.value())
            except KeyError as e:
                print(f"Failed to unpack message {e}")
        await asyncio.sleep(1.0)


def main():
    """Checks for topic and creates the topic if it does not exist"""
    try:
        asyncio.run(produce_consume("com.udacity.lesson3.exercise4.clicks"))
    except KeyboardInterrupt as e:
        print("shutting down")


async def produce_consume(topic_name):
    """Runs the Producer and Consumer tasks"""
    t1 = asyncio.create_task(produce(topic_name))
    t2 = asyncio.create_task(consume(topic_name))
    await t1
    await t2


if __name__ == "__main__":
    main()
