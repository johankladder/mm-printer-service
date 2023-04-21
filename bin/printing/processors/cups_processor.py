from bin.printing.handler import PrintProcessor
from bin.models.print_payload import PrintPayload

from service.mqtt.publishers.status_publisher import StatusPublisher

from bin.util.cups import CupsConnection

import cups
import time
import os


class CupsProcessor(PrintProcessor):

    options = {
        "fit-to-page": "True",
    }

    def print_page(self, print_payload: PrintPayload, path: str):
        with CupsConnection() as conn:
            default_media_size = conn.getPrinterAttributes(
                print_payload.printer).get("media-default", "na_letter")
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

                time.sleep(2)
