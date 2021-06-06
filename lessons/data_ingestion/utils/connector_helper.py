from lessons.data_ingestion.utils.kafka_connect_helper import KafkaConnectHelper

CONNECT_ENDPOINTS = {
    "plugins": "/connector-plugins",
    "connectors": "/connectors"
}


class ConnectorHelper(KafkaConnectHelper):
    """
    Helper class for Kafka Connect Connector API endpoints. If verbose is set to True, every request
    will pretty print the method, endpoint, status code, and response
    """

    def __init__(self, connector_name=None, plugin_name=None, verbose=False):

        super().__init__()
        self.connector_name = connector_name
        self.plugin_name = plugin_name
        self.verbose = verbose

    def get_connector_details(self, name):
        """
        Returns details about connector `name`
        :return: json response
        """
        endpoint = f"{CONNECT_ENDPOINTS['connectors']}/{name}"
        r = self.request(endpoint=endpoint)
        return r.json()

    def get_connectors(self):
        """
        Returns a list of connectors
        :return: list
        """
        r = self.request(endpoint=CONNECT_ENDPOINTS["connectors"])
        return r.json()

    def get_plugins(self):
        """
        Returns a dict of plugins
        :return: json response
        """
        r = self.request(endpoint=CONNECT_ENDPOINTS["plugins"])
        return r.json()

    def create_connector(self, name, conn_cls, max_tasks, logpath, topic):
        """
        Creates a new connector
        :return: json response
        """
        connectors = self.get_connectors()
        if name in connectors:
            raise ValueError(f"Connector {name} already exists. Current connectors: {connectors}")

        data = {
            "name": name,
            "config": {
                "connector.class": conn_cls,
                "tasks.max": max_tasks,
                "file": logpath,
                "topic": topic
            }
        }

        r = self.request(method="post", endpoint=CONNECT_ENDPOINTS["connectors"], data=data)
        return r.json()

    def manage_connector(self, name, action):
        """
        Pause, restart, or delete a connector
        :param name: the name of the connector
        :param action: One of "pause", "restart", "delete"
        :return: json response
        """
        actions = {
            "pause": "PUT",
            "resume": "PUT",
            "restart": "POST",
            "delete": "DELETE"
        }
        if not actions.get(action):
            raise ValueError(f"Connector `name` must be one of: {actions.keys()}")

        if action == "delete":
            endpoint = f"/connectors/{name}"
        else:
            endpoint = f"/connectors/{name}/{action}"

        r = self.request(endpoint=endpoint, method=actions[action])
        return r.json()

    def get_connector_status(self, name):
        """
        Get the status of a connector
        :param name: the name of the connector
        :return: json response
        """
        endpoint = f"/connectors/{name}/status"
        r = self.request(endpoint=endpoint)
        return r.json()
