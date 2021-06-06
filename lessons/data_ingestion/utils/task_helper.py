from lessons.data_ingestion.utils.kafka_connect_helper import KafkaConnectHelper

TASK_ENDPOINTS = {
    "tasks": "/connectors/{conn_name}/tasks",
    "status": "/connectors/{conn_name}/tasks/{task_id}/status",
    "restart": "/connectors/{conn_name}/tasks/{task_id}/restart",

}


class TaskHelper(KafkaConnectHelper):
    """
    Helper class for Kafka Task Connector API endpoints. If verbose is set to True, every request
    will pretty print the method, endpoint, status code, and response
    """

    def __init__(self, conn_name, task_id=None, verbose=False):
        """
        Initialize a TaskHelper object. `conn_name` is required for all endpoints
        :param conn_name: Required; the name of the connector
        :param task_id: Optional; the name of the task
        """
        super().__init__()
        self.conn_name = conn_name
        self.task_id = task_id
        self.verbose = verbose

    def task_details(self):
        """
        Returns details about task `name`
        :return: json response
        """
        endpoint = TASK_ENDPOINTS["tasks"].format(conn_name=self.conn_name)
        return self.request(endpoint=endpoint, method="get").json()

    def task_status(self, task_id):
        """
        Gets a task's status
        :return: list
        """
        endpoint = TASK_ENDPOINTS["status"].format(conn_name=self.conn_name, task_id=task_id)
        return self.request(endpoint=endpoint, method="get").json()

    def restart_task(self, task_id):
        """
        Restart a task
        :return: json response
        """
        endpoint = TASK_ENDPOINTS["restart"].format(conn_name=self.conn_name, task_id=task_id)
        return self.request(endpoint=endpoint, method="get").json()
