from flask import Blueprint, request
import cups
import subprocess

cups_views = Blueprint('cups-views', __name__)


@cups_views.route("/cups/cancel-all-jobs", methods=['POST'])
def cancel_all():
    conn = cups.Connection()
    jobs = conn.getJobs()
    for job_id, job_attributes in jobs.items():
        conn.cancelJob(job_id)
    return "OK"


@cups_views.route("/cups/cancel-jobs", methods=['POST'])
def cancel_jobs():
    queue = request.json["queue_name"]
    conn = cups.Connection()
    conn.cancelAllJobs(queue)
    return "OK"


@cups_views.route("/cups/printers", methods=['GET'])
def get_all_printers():

    lpstat_output = subprocess.check_output(['lpstat', '-a'], text=True)

    # Split the output by lines
    lpstat_lines = lpstat_output.splitlines()

    printers = []
    for line in lpstat_lines:
        printer_name = line.split()[0]
        printers.append({
            "queue_name": printer_name
        })

    return printers
