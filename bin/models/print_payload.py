
class PrintPayload():

    def __init__(self, printer: str, base64: str, pages: dict[int], identifier: int = None) -> None:
        self.printer = printer
        self.base64 = base64
        self.pages = pages
        self.identifier = identifier
