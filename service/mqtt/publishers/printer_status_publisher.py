import os
import json

from paho.mqtt.client import Client

class PrinterStatusPublisher():

    def __init__(self, client: Client) -> None:
        self.client = client

    def get_topic(self, printer_name):
        status_topic = os.getenv(
            "PRINTER_STATUS_TOPIC", 'mm/printing/printer/status/+')
        return status_topic.replace('+', printer_name)

    def publish(self, printer_name: str, status: int):
        topic = self.get_topic(printer_name=printer_name)
        payload = {
            "status": status
        }
        self.client.publish(topic, payload=json.dumps(payload))
