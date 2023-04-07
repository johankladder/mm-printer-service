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

    def publish(self, print_payload: PrintPayload, status: str):
        topic = self.get_topic(print_payload=print_payload)
        payload = {
            "status": status,
            "printer": {
                "id": print_payload.printer.id,
                "name": print_payload.printer.readable_name
            }
        }
        self.client.publish(topic, payload=json.dumps(payload))
