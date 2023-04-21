from flask import Blueprint, request

from bin.util.cups import get_all_cups_printers

from service.mqtt.runner import get_connected_client

import os
import json

from bin.util.cups import CupsConnection

cups_views = Blueprint('cups-views', __name__)


@cups_views.route("/cups/cancel-all-jobs", methods=['POST'])
def cancel_all():
    with CupsConnection() as conn:
        jobs = conn.getJobs()
        for job_id, job_attributes in jobs.items():
            conn.cancelJob(job_id)
        return "OK"


@cups_views.route("/cups/cancel-jobs", methods=['POST'])
def cancel_jobs():
    with CupsConnection() as conn:
        queue = request.json["queue_name"]
        conn.cancelAllJobs(queue)
        return "OK"


@cups_views.route("/cups/printers", methods=['GET'])
def get_all_printers():
    printers = []
    for cup_printer in get_all_cups_printers():
        printers.append({
            "queue_name": cup_printer
        })
    return printers


@cups_views.route("/cups/test-page", methods=['POST'])
def print_test_page():
    client = get_connected_client()
    print_topic = os.getenv(
        "PRINT_TOPIC", 'mm/printing/print/+').replace('+', 'test-page')
    queue_name = request.json["queue_name"]
    payload = {
        "url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        "printer": queue_name,
        "pages": [0],
        "id": "test"
    }

    client.publish(print_topic, json.dumps(payload))
    return "OK"
