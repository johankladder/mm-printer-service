import subprocess
import cups
import re


def get_all_cups_printers():
    lpstat_output = subprocess.check_output(['lpstat', '-a'], text=True)
    filtered_output = subprocess.check_output(['grep', 'printer'], input=lpstat_output, text=True)

    # Split the output by lines
    lpstat_lines = filtered_output.splitlines()

    printers = []
    for line in lpstat_lines:
        printer_name = line.split()[0]
        printers.append(printer_name)

    return printers


def get_printer_state(printer_name):

    printer_states = {
        'idle': 3,
        'printing': 4,
        'stopped': 5
    }

    # Execute the lpstat command and capture its output
    lpstat_output = subprocess.check_output(
        ['lpstat', '-p', printer_name]).decode().strip()

    # Use a regular expression to extract the printer status
    match = re.search(r'(?:is|now)\s+(\w+)', lpstat_output)

    if match:
        printer_status = match.group(1)
    else:
        printer_status = None

    # Map the printer status to the corresponding integer value
    if printer_status in printer_states:
        status_code = printer_states[printer_status]

    # Only return -1 status when status was not in mapping
    return -1 if printer_status is None else status_code

class CupsConnection:
    def __enter__(self):
        self.conn = cups.Connection()
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn = None
