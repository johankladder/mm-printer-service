
# Run file with: python -m service.mqtt.runner

import os
import threading
import time

from bin.processing.generator import PDFGenerator
from bin.processing.merger import PDFMerger
from bin.processing.payload_parser import PayloadParser

from bin.models.print_payload import PrintPayload

from bin.printing.handler import PrintHandler, PrintProcessor
from bin.printing.processors.debug_processor import DebugProcessor
from bin.printing.processors.cups_processor import CupsProcessor


from service.mqtt.publishers.error_publisher import ErrorPublisher

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

payload_parser = PayloadParser()
generator = PDFGenerator()
merger = PDFMerger()


def get_connected_client():
    location = os.getenv("MQTT_HOST", 'localhost')
    port = int(os.getenv("MQTT_PORT", 1883))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.username_pw_set(
        username=os.getenv("MQTT_USER", ''),
        password=os.getenv("MQTT_PASSWORD", '')
    )

    client.connect(location, port, 60)
    return client


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    print_topic: str = os.getenv("PRINT_TOPIC", 'mm/printing/print/+')
    client.subscribe(print_topic)
    client.message_callback_add(print_topic, on_print_data)


def on_print_data(client, userdata, msg):

    print("received")

    def process_message():
        topic_id = msg.topic.split("/")[3]

        processor_map = {
            'debug': DebugProcessor(client),
            'cups': CupsProcessor(client)
        }

        processors_from_env: list[str] = os.getenv(
            "PROCESSORS", 'debug').split(',')

        processors = []

        for processor in processors_from_env:
            processors.append(processor_map[processor])

        try:
            handler = PrintHandler(
                processors
            )

            print_payload: PrintPayload = payload_parser.parse_payload(
                msg.payload
            )
            print_payload.identifier = topic_id

            base_pdf = generator.generate(payload=print_payload)
            merged_pdf = merger.merge(
                pdf=base_pdf, pages=print_payload.pages, exclude=print_payload.exclude)
            handler.print(print_payload=print_payload, pdf=merged_pdf)
        except BaseException as exception:
            print("Something went wrong (%s)" % (type(exception).__name__))
            ErrorPublisher(client).publish(
                topic_id=topic_id, exception=type(exception).__name__)

    # Make the processing non locking:
    t = threading.Thread(target=process_message)
    t.start()


if __name__ == "__main__":

    load_dotenv()

    client = get_connected_client()
    client.loop_start()

    # Keep open:
    while True:
        status_topic = os.getenv(
            "SERVICE_STATUS_TOPIC", 'mm/mqtt/printing/status')
        client.publish(status_topic, "")
        time.sleep(5)
