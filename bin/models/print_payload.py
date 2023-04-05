from bin.database.models import Printer


class PrintPayload():

    def __init__(self, printer: Printer, base64: str, pages: dict[int]) -> None:
        self.printer = printer
        self.base64 = base64
        self.pages = pages
