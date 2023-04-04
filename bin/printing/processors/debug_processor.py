
from bin.printing.handler import PrintProcessor


class DebugProcessor(PrintProcessor):

    def print_page(self, printer: any, path: str):
        print("DEBUG: Print path " + path + " to printer" + printer)
