
import os

from bin.printing.handler import PrintProcessor
from bin.database.models import Printer


class CupsProcessor(PrintProcessor):

    def print_page(self, printer: Printer, path: str):
        commands = ["lp", path, '-d ' + printer.progressor_identifier]
        command = " ".join(commands)
        os.system(command)
