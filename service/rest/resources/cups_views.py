from flask import Blueprint, request

from bin.util.cups import get_all_cups_printers

from service.mqtt.runner import get_connected_client

import os
import cups
import subprocess
import json

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
        "base64": "JVBERi0xLjcKCjEgMCBvYmogICUgZW50cnkgcG9pbnQKPDwKICAvVHlwZSAvQ2F0YWxvZwogIC9QYWdlcyAyIDAgUgo+PgplbmRvYmoKCjIgMCBvYmoKPDwKICAvVHlwZSAvUGFnZXMKICAvTWVkaWFCb3ggWyAwIDAgMjAwIDIwMCBdCiAgL0NvdW50IDEKICAvS2lkcyBbIDMgMCBSIF0KPj4KZW5kb2JqCgozIDAgb2JqCjw8CiAgL1R5cGUgL1BhZ2UKICAvUGFyZW50IDIgMCBSCiAgL1Jlc291cmNlcyA8PAogICAgL0ZvbnQgPDwKICAgICAgL0YxIDQgMCBSIAogICAgPj4KICA+PgogIC9Db250ZW50cyA1IDAgUgo+PgplbmRvYmoKCjQgMCBvYmoKPDwKICAvVHlwZSAvRm9udAogIC9TdWJ0eXBlIC9UeXBlMQogIC9CYXNlRm9udCAvVGltZXMtUm9tYW4KPj4KZW5kb2JqCgo1IDAgb2JqICAlIHBhZ2UgY29udGVudAo8PAogIC9MZW5ndGggNDQKPj4Kc3RyZWFtCkJUCjcwIDUwIFRECi9GMSAxMiBUZgooSGVsbG8sIHdvcmxkISkgVGoKRVQKZW5kc3RyZWFtCmVuZG9iagoKeHJlZgowIDYKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDEwIDAwMDAwIG4gCjAwMDAwMDAwNzkgMDAwMDAgbiAKMDAwMDAwMDE3MyAwMDAwMCBuIAowMDAwMDAwMzAxIDAwMDAwIG4gCjAwMDAwMDAzODAgMDAwMDAgbiAKdHJhaWxlcgo8PAogIC9TaXplIDYKICAvUm9vdCAxIDAgUgo+PgpzdGFydHhyZWYKNDkyCiUlRU9G",
        "printer": queue_name,
        "pages": [0],
        "id": "test"
    }

    client.publish(print_topic, json.dumps(payload))
    return "OK"
