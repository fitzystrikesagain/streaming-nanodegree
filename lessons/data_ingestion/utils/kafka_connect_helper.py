import json
from json.decoder import JSONDecodeError
from pprint import pprint
import requests

from lessons.data_ingestion.utils.constants import CONNECT_BASE_URL as BASE_URL
from lessons.data_ingestion.utils.constants import CONNECT_HEADERS as HEADERS


class KafkaConnectHelper:
    """
    Parent helper class for KafkaConnect REST API. Can be used to create classes for Connectors, Tasks, etc.
    """
    def __init__(self, verbose=False):
        self.verbose = verbose

    def request(self, endpoint="", method="get", data=None):
        """
        Request handler for Kafka Connect API
        :return: json response
        """
        data = self.serialize(data) if data else {}
        url = BASE_URL if not endpoint else BASE_URL + endpoint
        r = requests.request(url=url, method=method, headers=HEADERS, data=data)
        if self.verbose:
            pprint(f"{method} {BASE_URL}{endpoint}")
            pprint(f"Status code: {r.status_code}")
            try:
                pprint(r.json())
            # If there is no json, don't print the error
            except JSONDecodeError as e:
                pass
            print()
        return r

    @staticmethod
    def serialize(json_data):
        """
        Serialize json object to string
        :param json_data: a json payload
        :return: string
        """
        return json.dumps(json_data)
