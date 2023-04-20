
class PrintPayload():

    def __init__(self, printer: str,  pages: dict[int], base64: str = None,  url: str = None, identifier: int = None, exclude: bool = False) -> None:
        self.printer = printer
        self.base64 = base64
        self.pages = pages
        self.identifier = identifier
        self.exclude = exclude
        self.url = url
