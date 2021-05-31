import asyncio

from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient, NewTopic

BROKER_URL = "PLAINTEXT://localhost:9092"
TOPIC_NAME = "my-first-python-topic"
SLEEP_DURATION = 1.0


async def produce(topic_name=TOPIC_NAME):
    """Produces data into the Kafka Topic"""
    p = Producer({"bootstrap.servers": BROKER_URL})

    curr_iteration = 0
    while True:
        p.produce(topic_name, f"Message: {curr_iteration}")

        curr_iteration += 1
        await asyncio.sleep(SLEEP_DURATION)


async def consume(topic_name=TOPIC_NAME):
    """Consumes data from the Kafka Topic"""
    c = Consumer({"bootstrap.servers": BROKER_URL,
                  "group.id": "first-python-consumer_group"})

    c.subscribe([topic_name])

    while True:
        message = c.poll(timeout=1.0)

        if not message:
            print("No message received")
        elif message.error():
            print(f"Message had an error: {message.error()}")
        else:
            print(f"Key: {message.key()}, Value: {message.value()}")

        await asyncio.sleep(SLEEP_DURATION)


async def produce_consume():
    """Runs the Producer and Consumer tasks"""
    t1 = asyncio.create_task(produce(TOPIC_NAME))
    t2 = asyncio.create_task(consume(TOPIC_NAME))
    await t1
    await t2


def main():
    """Runs the exercise"""
    client = AdminClient({"bootstrap.servers": BROKER_URL})
    topic = NewTopic(TOPIC_NAME, num_partitions=1, replication_factor=1)

    client.create_topics([topic])

    try:
        asyncio.run(produce_consume())
    except KeyboardInterrupt as e:
        print("shutting down")
    finally:
        client.delete_topics([topic])
        pass


if __name__ == "__main__":
    main()
