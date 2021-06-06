from lessons.data_ingestion.utils.connector_helper import ConnectorHelper
from lessons.data_ingestion.utils.task_helper import TaskHelper


def connector_demo():
    # Create a helper object
    helper = ConnectorHelper(verbose=True)
    connector_name = "first-connector"

    # Show current plugins
    helper.get_plugins()

    # Configure a new connector
    try:
        helper.create_connector(
            name=connector_name,
            conn_cls="FileStreamSource",
            max_tasks=1,
            logpath="/var/log/journal/confluent-kafka-connect.service.log",
            topic="kafka-connect-logs"
        )
    except ValueError as e:
        print(e)

    # Show current connectors
    helper.get_connectors()

    # Get connector details
    helper.get_connector_details(connector_name)

    # Get a connector's status
    helper.get_connector_status(name=connector_name)

    helper.manage_connector(name=connector_name, action="pause")
    # Pause a connector
    try:
        helper.manage_connector(name=connector_name, action="pause")
    except ValueError as e:
        print(e)

    # Unpause a connector
    try:
        helper.manage_connector(name=connector_name, action="resume")
    except ValueError as e:
        print(e)

    # Restart a connector
    try:
        helper.manage_connector(name=connector_name, action="restart")
    except ValueError as e:
        print(e)

    # Delete a connector
    try:
        helper.manage_connector(name=connector_name, action="delete")
    except ValueError as e:
        print(e)


def task_demo():
    # First, create a new connector
    my_conn = ConnectorHelper(connector_name="first-connector", verbose=True)

    try:
        my_conn.create_connector(
            name=my_conn.connector_name,
            conn_cls="FileStreamSource",
            max_tasks=1,
            logpath="/var/log/journal/confluent-kafka-connect.service.log",
            topic="kafka-connect-logs"
        )
    except ValueError as e:
        print(e)

    # Show the connector's tasks (will be empty list if no tasks)
    my_task = TaskHelper(conn_name=my_conn.connector_name, verbose=True)
    my_task.task_details()


if __name__ == "__main__":
    connector_demo()
    # task_demo()
    pass
