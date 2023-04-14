
from bin.printing.handler import PrintProcessor
from bin.models.print_payload import PrintPayload

from service.mqtt.publishers.status_publisher import StatusPublisher

import cups
import time

class CupsProcessor(PrintProcessor):

    options = {
        "fit-to-page": "True",
        "landscape": "True",
    }

    def print_page(self, print_payload: PrintPayload, path: str):
        conn = cups.Connection()

        # Retrieve media format of label printer:
        attributes = conn.getPrinterAttributes(print_payload.printer)
        default_media_size = attributes.get("media-default", "na_letter")
        self.options["media"] = default_media_size

        job_id = conn.printFile(
            print_payload.printer,
            path,
            'Print job',
            self.options
        )

        completed = False
        stopped = False
        status = None

        while not completed and not stopped:
            job = conn.getJobAttributes(job_id)
            job_state = job.get('job-state', None)

            if job_state == 3:
                status = "HELD"
            elif job_state == 5:
                status = "PROCESSING"
            elif job_state == 7:
                status = "STOPPED"
                stopped = True
            elif job_state == 9:
                status = "COMPLETED"
                completed = True
            else:
                status = "UNKNOWN"

            StatusPublisher(self.client).publish(
                print_payload=print_payload,
                status=status
            )

            time.sleep(0.5)
