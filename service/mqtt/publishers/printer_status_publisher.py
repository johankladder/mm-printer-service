import json

from paho.mqtt.client import Client


class PrinterStatusPublisher():
    
    def publish(self, client: Client, topic, status: int):
        payload = {
            "status": status
        }
        client.publish(topic, payload=json.dumps(payload), qos=0, retain=False)


class StatusPublisherContext:

    def __enter__(self):
        self.conn = PrinterStatusPublisher()
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn = None