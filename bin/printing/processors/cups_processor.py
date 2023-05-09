from bin.printing.handler import PrintProcessor
from bin.models.print_payload import PrintPayload

from service.mqtt.publishers.status_publisher import StatusPublisher
from bin.util.cups import CupsConnection, get_printer_state
import time

class CupsProcessor(PrintProcessor):

    options = {
        "fit-to-page": "True",
    }

    def print_page(self, print_payload: PrintPayload, path: str):
        with CupsConnection() as conn:
            default_media_size = conn.getPrinterAttributes(
                print_payload.printer).get("media-default", "na_letter")
            self.options["media"] = default_media_size

            conn.printFile(
                print_payload.printer,
                path,
                'Print job',
                self.options
            )

            completed = False
            stopped = False
            status = None

            while not completed and not stopped:

                state = get_printer_state(print_payload.printer)

                if state == 4:
                    status = "PROCESSING"
                elif state == 3:
                    status = "COMPLETED"
                    completed = True
                elif state == 5:
                    status = "STOPPED"
                    stopped = True
                else:
                    status = "UNKNOWN"

                StatusPublisher(self.client).publish(
                    print_payload=print_payload,
                    status=status
                )

                time.sleep(2)
