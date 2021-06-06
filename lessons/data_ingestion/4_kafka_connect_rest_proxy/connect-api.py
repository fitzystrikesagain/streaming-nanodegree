from lessons.data_ingestion.utils.connector_helper import ConnectorHelper


def main():
    # Create a helper object
    helper = ConnectorHelper(verbose=True)

    # Show current plugins
    helper.get_plugins()

    # Configure a new connector
    connector_name = "first-connector"
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


if __name__ == "__main__":
    main()
