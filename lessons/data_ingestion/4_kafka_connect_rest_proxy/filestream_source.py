import asyncio
import json

import requests

from lessons.data_ingestion.utils.constants import CONNECT_BASE_URL
from lessons.data_ingestion.utils.connector_helper import ConnectorHelper

KAFKA_CONNECT_URL = f"{CONNECT_BASE_URL}/connectors"
CONNECTOR_NAME = "exercise2"
helper = ConnectorHelper(connector_name=CONNECTOR_NAME, verbose=True)


def configure_connector():
    """Calls Kafka Connect to create the Connector"""
    print("creating or updating kafka connect connector...")

    try:
        helper.create_connector(
            name="local-file-source",
            conn_cls="FileStreamSource",
            max_tasks=1,
            logpath="/tmp/test.txt",
            topic="connect-test",
            key_converter="org.apache.kafka.connect.json.JsonConverter",
            key_converter_schemas_enable="false",
            value_converter="org.apache.kafka.connect.json.JsonConverter",
            value_converter_schemas_enable="false"
        )
    except ValueError as e:
        exit(e)


async def log():
    """Continually appends to the end of a file"""
    with open(f"/tmp/{CONNECTOR_NAME}.log", "w") as f:
        iteration = 0
        while True:
            f.write(f"log number {iteration}\n")
            f.flush()
            await asyncio.sleep(1.0)
            iteration += 1


async def log_task():
    """Runs the log task"""
    task = asyncio.create_task(log())
    configure_connector()
    await task


def run():
    """Runs the simulation"""
    try:
        asyncio.run(log_task())
    except KeyboardInterrupt as e:
        print("shutting down")


if __name__ == "__main__":
    run()
