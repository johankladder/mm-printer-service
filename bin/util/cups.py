import subprocess

def get_all_cups_printers():
    lpstat_output = subprocess.check_output(['lpstat', '-a'], text=True)

    # Split the output by lines
    lpstat_lines = lpstat_output.splitlines()

    printers = []
    for line in lpstat_lines:
        printer_name = line.split()[0]
        printers.append(printer_name)
    return printers