import os
import json

from paho.mqtt.client import Client

class PrinterStatusPublisher():

    def __init__(self, printer_name: str) -> None:
        self.printer_name = printer_name
        self.status_topic = os.getenv(
            "PRINTER_STATUS_TOPIC", 'mm/printing/printer/status/+').replace('+', printer_name)

    def publish(self, client: Client, status: int):
        payload = {
            "status": status
        }
        client.publish(self.status_topic, payload=json.dumps(payload), qos=0, retain=False)
