
from bin.printing.handler import PrintProcessor
from bin.models.print_payload import PrintPayload
from bin.processing.extractor import PDFExtractor

from service.mqtt.publishers.status_publisher import StatusPublisher


class DebugProcessor(PrintProcessor):

    def print_page(self, print_payload: PrintPayload, path: str):
        pdf = PDFExtractor().extract(path)

        print("DEBUG: Print path: %s" % (path))
        print("DEBUG: Printing on printer: %s" %
              (print_payload.printer))
        print("DEBUG: Printing: %i pages" % (len(pdf.pages)))

        StatusPublisher(self.client).publish(
            print_payload=print_payload,
            status="DEBUGGED"
        )
