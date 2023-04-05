
# Run file with: python -m service.mqtt.runner

import os
import threading

from bin.processing.generator import PDFGenerator
from bin.processing.merger import PDFMerger
from bin.processing.payload_parser import PayloadParser

from bin.models.print_payload import PrintPayload

from bin.printing.handler import PrintHandler
from bin.printing.processors.debug_processor import DebugProcessor
from bin.printing.processors.cups_processor import CupsProcessor

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

payload_parser = PayloadParser()
generator = PDFGenerator()
merger = PDFMerger()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    print_topic: str = os.getenv("PRINT_TOPIC", 'mm/printing/print/+')
    print_status_topic: str = os.getenv(
        "PRINT_STATUS_TOPIC", 'mm/printing/status/+')
    client.subscribe(print_topic)
    client.subscribe(print_status_topic)
    client.message_callback_add(print_topic, on_print_data)
    client.message_callback_add(print_status_topic, on_print_status_data)


def on_print_status_data(client, userdata, msg):
    print("Recieved message on topic '%s' | Payload: %s" % (msg.topic, msg.payload))


def on_print_data(client, userdata, msg):

    def process_message():
        print("Recieved message on topic '%s'" % (msg.topic))
        topic_id = msg.topic.split("/")[3]

        try:
            handler = PrintHandler(
                processors=[
                    DebugProcessor(client),
                    CupsProcessor(client)
                ]
            )

            print_payload: PrintPayload = payload_parser.parse_payload(
                msg.payload
            )
            print_payload.identifier = topic_id

            base_pdf = generator.generate(base64=print_payload.base64)
            merged_pdf = merger.merge(pdf=base_pdf, pages=print_payload.pages)
            handler.print(print_payload=print_payload, pdf=merged_pdf)
        except BaseException as exception:
            print("Something went wrong (%s)" % (type(exception).__name__))

    # Make the processing non locking:
    t = threading.Thread(target=process_message)
    t.start()


if __name__ == "__main__":

    load_dotenv()

    location = os.getenv("MQTT_HOST", 'localhost')
    port = int(os.getenv("MQTT_PORT", 1883))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.username_pw_set(
        username=os.getenv("MQTT_USER", ''),
        password=os.getenv("MQTT_PASSWORD", '')
    )

    client.connect(location, port, 60)
    client.loop_start()

    # Keep open:
    while True:
        pass
