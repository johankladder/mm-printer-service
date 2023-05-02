import subprocess
import cups

def get_all_cups_printers():
    lpstat_output = subprocess.check_output(['lpstat', '-a'], text=True)

    # Split the output by lines
    lpstat_lines = lpstat_output.splitlines()

    printers = []
    for line in lpstat_lines:
        printer_name = line.split()[0]
        if 'printer' in printer_name:
            printers.append(printer_name)
    return printers


class CupsConnection:
    def __enter__(self):
        self.conn = cups.Connection()
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn = None