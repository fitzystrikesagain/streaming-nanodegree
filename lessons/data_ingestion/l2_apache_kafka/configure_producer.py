from dataclasses import dataclass, field, asdict
import json
import random
import time

from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from faker import Faker

faker = Faker()

BROKER_URL = "PLAINTEXT://localhost:9092"
TOPIC_NAME = "com.udacity.streams.purchases"


@dataclass
class Purchase:
    username: str = field(default_factory=faker.user_name)
    currency: str = field(default_factory=faker.currency_code)
    amount: int = field(default_factory=lambda: random.randint(100, 200000))

    def serialize(self):
        """Serializes the object in JSON string format"""
        return json.dumps(asdict(self))


def create_topic(topic):
    """Creates the topic with the given topic name"""
    client = AdminClient({"bootstrap.servers": BROKER_URL})
    futures = client.create_topics(
        [NewTopic(topic=topic, num_partitions=5, replication_factor=1)]
    )
    for _, future in futures.items():
        try:
            future.result()
        except Exception as e:
            pass


def produce_sync(topic_name):
    """Produces data synchronously into the Kafka Topic"""
    p = Producer({
        "bootstrap.servers": BROKER_URL,
        # "linger.ms": "10000",
        # "batch.num.messages": "10000",
        # "queue.buffering.max.messages": "1000000",
        # "compression.type": "snappy"
    })
    # start_time = datetime.utcnow()
    # curr_iteration = 0

    while True:
        p.produce(topic_name, Purchase().serialize())
        # if curr_iteration % 10000 == 0:
        #     elapsed = (datetime.utcnow() - start_time).seconds
        #     print(f"Msgs sent: {curr_iteration} | Seconds elapsed: {elapsed}")
        # curr_iteration += 1

        """
        We call poll here to flush message delivery reports from Kafka.
        We don't care about the details, so calling it with a timeout of 0s
        means it returns immediately and has very little performance impact.
        """
        p.poll(0)
        time.sleep(.5)


def main():
    """Checks for topic and creates the topic if it does not exist"""
    create_topic(TOPIC_NAME)
    try:
        produce_sync(TOPIC_NAME)
    except KeyboardInterrupt as e:
        print("shutting down")
        print(e)


if __name__ == "__main__":
    main()
