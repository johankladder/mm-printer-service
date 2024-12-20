
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

from bin.util.cups import get_all_cups_printers

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

payload_parser = PayloadParser()
generator = PDFGenerator()
merger = PDFMerger()

processors = []
printer_queues = {}

threads = []
running = True

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
    if rc == 0:
        fill_processors(client=client)
        construct_printer_queues()
        print_topic: str = os.getenv("PRINT_TOPIC", 'mm/printing/print/+')
        client.subscribe(print_topic)
        client.message_callback_add(print_topic, on_received_message_print_topic)


def fill_processors(client):
    processor_map = {
        'debug': DebugProcessor(client),
        'cups': CupsProcessor(client)
    }

    processors_from_env: list[str] = os.getenv(
        "PROCESSORS", 'debug').split(',')

    # Clear the list and fill it with the processors from the environment
    processors.clear()

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
        threads.append(queue_thread)

def process_printer_messages(printer_name, queue):
    """
    This function is called in the 'queue thread' and handles, parses and dispatches 
    incoming payload for printing to cups. 
    """

    while running:
        try:
            print_payload: PrintPayload = queue.get(timeout=1)
        except:
            continue

        try:
            handler = PrintHandler(processors)
            base_pdf = generator.generate(payload=print_payload)
            merged_pdf = merger.merge(
                pdf=base_pdf, pages=print_payload.pages, exclude=print_payload.exclude)
            handler.print(print_payload=print_payload, pdf=merged_pdf)
        except BaseException as exception:
            pass


def on_received_message_print_topic(client, userdata, msg):
    try:
        print("received print topic!")

        # 1.  Processing payload that was received:
        print_payload: PrintPayload = payload_parser.parse_payload(msg.payload)
        topic_id = msg.topic.split("/")[3]
        print_payload.identifier = topic_id

        # 2. Inject this payload in printer queue:
        printer_queues[print_payload.printer].put(print_payload)

    except BaseException as exception:
        pass


if __name__ == "__main__":

    load_dotenv()

    try:
        client = get_connected_client()
        print("Starting client...")
        client.loop_forever()

    except KeyboardInterrupt:
        print("Exiting...")
        running = False
    finally:
        print("Stopping threads...")
        for thread in threads:
            thread.join()

        print("Stopping client...")
        client.loop_stop()
        client.disconnect()

