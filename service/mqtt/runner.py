
import os

from bin.processing.generator import PDFGenerator
from bin.processing.merger import PDFMerger
from bin.processing.payload_parser import PayloadParser

from bin.models.print_payload import PrintPayload

from bin.printing.handler import PrintHandler
from bin.printing.processors.debug_processor import DebugProcessor

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

payload_parser = PayloadParser()
generator = PDFGenerator()
merger = PDFMerger()
handler = PrintHandler(
    processor=DebugProcessor()
)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    print_topic: str = os.getenv("PRINT_TOPIC", 'mm/printing/labels')
    client.subscribe(print_topic)


def on_message(client, userdata, msg):
    print("\n")
    print("Recieved message on topic '%s'" % (msg.topic))
    
    try:
        print_payload: PrintPayload = payload_parser.parse_payload(msg.payload)
        base_pdf = generator.generate(base64=print_payload.base64)
        merged_pdf = merger.merge(pdf=base_pdf, pages=print_payload.pages)
        handler.print(printer=print_payload.printer, pdf=merged_pdf)
    except BaseException as exception:
        print("Something went wrong (%s)" % (type(exception).__name__))


if __name__ == "__main__":

    load_dotenv()

    location = os.getenv("MQTT_HOST", 'localhost')
    port = int(os.getenv("MQTT_PORT", 1883))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(
        username=os.getenv("MQTT_USER", ''),
        password=os.getenv("MQTT_PASSWORD", '')
    )

    client.connect(location, port, 60)
    client.loop_forever()
