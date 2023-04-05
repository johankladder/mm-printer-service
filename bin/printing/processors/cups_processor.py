
import os

from bin.printing.handler import PrintProcessor
from bin.database.models import Printer

import cups
import time

class CupsProcessor(PrintProcessor):

    def print_page(self, printer: Printer, path: str):

        conn = cups.Connection()
        print("CUPS: Connected to cups")

        job_id = conn.printFile(
            printer.progressor_identifier,
            path,
            'test',
            {}
        )

        print("CUPS: Printing file with job id: %s" % (job_id))

        completed = False
        stopped = False
        status = None

        while not completed and not stopped:
            job = conn.getJobAttributes(job_id)
            job_state = job.get('job-state', None)

            if job_state == 3:
                status = "HELD"
            elif job_state == 5:
                status = "Processing"
            elif job_state == 7:
                status = "STOPPED"
                stopped = True
            elif job_state == 9:
                status = "COMPLETED"
                completed = True
            else:
                status="UNKNOWN"

            print("CUPS: Status (%s)" % (status))    
            time.sleep(0.5)

        print("CUPS: Completed printing sequence with status: %s" % (status))
