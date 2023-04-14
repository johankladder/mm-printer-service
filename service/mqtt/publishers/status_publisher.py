import os
import json

from paho.mqtt.client import Client

from bin.models.print_payload import PrintPayload


class StatusPublisher():

    def __init__(self, client: Client) -> None:
        self.client = client

    def get_topic(self, print_payload: PrintPayload):
        status_topic = os.getenv("PRINT_STATUS_TOPIC", 'mm/printing/status/+')
        return status_topic.replace('+', str(print_payload.identifier))

    def publish(self, print_payload: PrintPayload, status: str, debug: dict = {}):
        topic = self.get_topic(print_payload=print_payload)
        payload = {
            "status": status,
            "printer": {
                "queue_name": print_payload.printer,
                "pages": print_payload.pages
            },
            "debug": json.dumps(debug)
        }
        self.client.publish(topic, payload=json.dumps(payload))
