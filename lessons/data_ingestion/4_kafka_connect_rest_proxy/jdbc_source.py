from dotenv import dotenv_values

from lessons.data_ingestion.utils.constants import CONNECT_BASE_URL
from lessons.data_ingestion.utils.connector_helper import ConnectorHelper

# .env file is in the project's root directory
config = dotenv_values("../../../.env")
POSTGRES_PASSWORD = config.get("POSTGRES_PASSWORD")

KAFKA_CONNECT_URL = f"{CONNECT_BASE_URL}/connectors"
CONNECTOR_NAME = "clicks-jdbc"


def configure_connector():
    """Calls Kafka Connect to create the Connector"""
    print("creating or updating kafka connect connector...")

    data = {
        "name": CONNECTOR_NAME,
        "config": {
            "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
            "topic.prefix": "connect-",
            "mode": "incrementing",
            "incrementing.column.name": "id",
            "table.whitelist": "clicks",
            "tasks.max": 1,
            "connection.url": "jdbc:postgresql://postgres-classroom:5432/classroom",
            "connection.user": "postgres",
            "key.converter": "org.apache.kafka.connect.json.JsonConverter",
            "key.converter.schemas.enable": "false",
            "value.converter": "org.apache.kafka.connect.json.JsonConverter",
            "value.converter.schemas.enable": "false",
            "connection.password": POSTGRES_PASSWORD,
        },
    }
    conn = ConnectorHelper(verbose=True)
    conn.create_jdbc_connector(data)
    conn.get_connectors()
    conn.get_connector_details(CONNECTOR_NAME)


if __name__ == "__main__":
    configure_connector()
