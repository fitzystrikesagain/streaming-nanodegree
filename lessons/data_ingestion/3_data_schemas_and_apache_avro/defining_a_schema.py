import asyncio

from confluent_kafka import Producer
from faker import Faker

from lessons.data_ingestion.utils.click_event import ClickEvent

faker = Faker()

BROKER_URL = "PLAINTEXT://localhost:9092"
TOPIC = "com.udacity.lesson3.exercise2.clicks"


async def produce(topic_name):
    """Produces data into the Kafka Topic"""
    p = Producer({"bootstrap.servers": BROKER_URL})
    while True:
        p.produce(topic_name, ClickEvent().serialize_avro())
        await asyncio.sleep(1.0)


def main():
    """Checks for topic and creates the topic if it does not exist"""
    try:
        asyncio.run(produce_consume(TOPIC))
    except KeyboardInterrupt as e:
        print("shutting down")


async def produce_consume(topic_name):
    """Runs the Producer and Consumer tasks"""
    await asyncio.create_task(produce(topic_name))


if __name__ == "__main__":
    main()
