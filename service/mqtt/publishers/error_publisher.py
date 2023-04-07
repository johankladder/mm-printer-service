import os
import json

from paho.mqtt.client import Client

class ErrorPublisher():

    def __init__(self, client: Client) -> None:
        self.client = client

    def get_topic(self, topic_id: str):
        status_topic = os.getenv("PRINT_STATUS_TOPIC", 'mm/printing/status/+')
        return status_topic.replace('+', topic_id)

    def publish(self, topic_id: str, exception: str):
        topic = self.get_topic(topic_id)
        payload = {
            "status": "ERROR",
            "exception": exception,
        }
        self.client.publish(topic, payload=json.dumps(payload))
