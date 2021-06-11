import json

import requests

REST_PROXY_URL = "http://localhost:8082"


def get_topics():
    """Gets topics from REST Proxy"""
    url = f"{REST_PROXY_URL}/topics"
    resp = requests.get(url)

    try:
        resp.raise_for_status()
    except:
        print(f"Failed to get topics {json.dumps(resp.json(), indent=2)})")
        return []

    print("Fetched topics from Kafka:")
    print(json.dumps(resp.json(), indent=2))
    return resp.json()


def get_topic(topic_name):
    """Get specific details on a topic"""
    print(topic_name)
    url = f"{REST_PROXY_URL}/topics/{topic_name}"
    print(url)
    resp = requests.get(url)

    # try:
    #     resp.raise_for_status()
    # except:
    #     print("Failed to get topics {json.dumps(resp.json(), indent=2)})")

    print("Fetched topics from Kafka:")
    print(json.dumps(resp.json(), indent=2))


def get_brokers():
    """Gets broker information"""
    url = f"{REST_PROXY_URL}/brokers"
    resp = requests.get(url)

    try:
        resp.raise_for_status()
    except:
        print("Failed to get brokers {json.dumps(resp.json(), indent=2)})")

    print("Fetched brokers from Kafka:")
    print(json.dumps(resp.json(), indent=2))


def get_partitions(topic_name, partition_id=None):
    """Prints partition information for a topic"""
    url = f"{REST_PROXY_URL}/topics/{topic_name}/partitions"
    if partition_id:
        url += f"/{str(partition_id)}"

    resp = requests.get(url)
    print("Fetched partitions from Kafka:")
    print(json.dumps(resp.json(), indent=2))


if __name__ == "__main__":
    topics = get_topics()
    get_topic(topics[0])
    get_brokers()
    get_partitions(topics[-1])
