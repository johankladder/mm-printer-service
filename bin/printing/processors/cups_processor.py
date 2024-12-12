from bin.printing.handler import PrintProcessor
from bin.models.print_payload import PrintPayload
from bin.util.cups import CupsConnection

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
