
# Run file with: python -m service.mqtt.runner

import os
import threading
import time
import queue

from bin.processing.generator import PDFGenerator
from bin.processing.merger import PDFMerger
from bin.processing.payload_parser import PayloadParser

from bin.models.print_payload import PrintPayload

from bin.printing.handler import PrintHandler
from bin.printing.processors.debug_processor import DebugProcessor
from bin.printing.processors.cups_processor import CupsProcessor

from service.mqtt.publishers.error_publisher import ErrorPublisher

from bin.util.cups import get_all_cups_printers

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

payload_parser = PayloadParser()
generator = PDFGenerator()
merger = PDFMerger()

processors = []
printer_queues = {}


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

    construct_processors(client=client)
    construct_printer_queues()

    print_topic: str = os.getenv("PRINT_TOPIC", 'mm/printing/print/+')
    client.subscribe(print_topic)
    client.message_callback_add(print_topic, on_received_message_print_topic)


def construct_processors(client):
    processor_map = {
        'debug': DebugProcessor(client),
        'cups': CupsProcessor(client)
    }

    processors_from_env: list[str] = os.getenv(
        "PROCESSORS", 'debug').split(',')

    for processor in processors_from_env:
        processors.append(processor_map[processor])


def construct_printer_queues():
    for printer in get_all_cups_printers():
        printer_queues[printer] = queue.Queue()

    # Create listeners in seperate threads, so no locking will happen:
    for printer_name, printer_queue in printer_queues.items():
        queue_thread = threading.Thread(target=process_printer_messages,
                             args=(printer_name, printer_queue))
        queue_thread.start()


def process_printer_messages(printer_name, queue):
    while True:
        print_payload: PrintPayload = queue.get()
        try:
            handler = PrintHandler(processors)
            base_pdf = generator.generate(payload=print_payload)
            merged_pdf = merger.merge(
                pdf=base_pdf, pages=print_payload.pages, exclude=print_payload.exclude)
            handler.print(print_payload=print_payload, pdf=merged_pdf)
        except BaseException as exception:
            print("Something went wrong (%s)" % (type(exception).__name__))
            ErrorPublisher(client).publish(
                topic_id=print_payload.identifier, exception=type(exception).__name__)


def on_received_message_print_topic(client, userdata, msg):

    try:
        # 1.  Processing payload that was received:
        print_payload: PrintPayload = payload_parser.parse_payload(msg.payload)
        topic_id = msg.topic.split("/")[3]
        print_payload.identifier = topic_id

        # 2. Inject this payload in printer queue:
        printer_queues[print_payload.printer].put(print_payload)

    except BaseException as exception:
        print("Something went wrong (%s)" % (type(exception).__name__))
        ErrorPublisher(client).publish(
            topic_id=topic_id, exception=type(exception).__name__)


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
