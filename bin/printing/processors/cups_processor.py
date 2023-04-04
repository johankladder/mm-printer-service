
import os

from bin.printing.handler import PrintProcessor


class CupsProcessor(PrintProcessor):

    def print_page(self, printer: any, path: str):
        commands = ["lp", path, '-d ' + printer]
        command = " ".join(commands)
        os.system(command)
