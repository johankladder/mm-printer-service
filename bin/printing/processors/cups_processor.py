
import os

from bin.printing.handler import PrintProcessor
from bin.models.print_payload import PrintPayload

import cups
import time


class CupsProcessor(PrintProcessor):

    def print_page(self, print_payload: PrintPayload, path: str):

        conn = cups.Connection()
        job_id = conn.printFile(
            print_payload.printer.progressor_identifier,
            path,
            'test',
            {}
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

            self.publish(print_payload=print_payload, status=status)
            time.sleep(0.5)

    def publish(self, print_payload: PrintPayload, status: str):
        status_topic = os.getenv("PRINT_STATUS_TOPIC", 'mm/printing/status/+')
        status_topic = status_topic.replace('+', str(print_payload.identifier))
        self.client.publish(status_topic, status)
