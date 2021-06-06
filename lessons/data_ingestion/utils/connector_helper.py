from lessons.data_ingestion.utils.kafka_connect_helper import KafkaConnectHelper

CONNECT_ENDPOINTS = {
    "plugins": "/connector-plugins",
    "connectors": "/connectors",
    "details": "/connectors/{conn_name}",
    "manage": "/connectors/{conn_name}/{action}",
    "delete": "/connectors/{conn_name}/delete",
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
        endpoint = CONNECT_ENDPOINTS["details"].format(conn_name=name)
        r = self.request(endpoint=endpoint)
        return r.json()

    def get_connectors(self):
        """
        Returns a list of connectors
        :return: list
        """
        endpoint = CONNECT_ENDPOINTS["connectors"]
        r = self.request(endpoint=endpoint)
        return r.json()

    def get_plugins(self):
        """
        Returns a dict of plugins
        :return: json response
        """
        endpoint = endpoint = CONNECT_ENDPOINTS["plugins"]
        r = self.request(endpoint=endpoint)
        return r.json()

    def create_connector(self, name, conn_cls, max_tasks, logpath, topic, **kwargs):
        """
        Creates a new connector
        :param name: name of the connector
        :param conn_cls: connector class
        :param max_tasks: max number of tasks
        :param logpath: path to the logfile to read
        :param topic: name of the Kafka topic
        :param kwargs: additional config parameters
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
        # If config kwargs are passed, replace underscores with periods and add them to data
        for key, value in kwargs.items():
            data["config"][key.replace("_", ".")] = value

        endpoint = CONNECT_ENDPOINTS["connectors"]
        r = self.request(method="post", endpoint=endpoint, data=data)
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
            endpoint = CONNECT_ENDPOINTS["delete"].format(conn_name=name)
        else:
            endpoint = CONNECT_ENDPOINTS["manage"].format(conn_name=name, action=action)
        r = self.request(endpoint=endpoint, method=actions[action])
        if action == "delete" and r.status_code == 404:
            print(f"Connector not found for action {action} {name}")
        return r

    def get_connector_status(self, name):
        """
        Get the status of a connector
        :param name: the name of the connector
        :return: json response
        """
        endpoint = f"/connectors/{name}/status"
        r = self.request(endpoint=endpoint)
        return r.json()
