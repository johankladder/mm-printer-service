from pypdf import PdfReader
from bin.database.models import Printer


class PrintProcessor():

    def print_page(self, printer: Printer, path: str):
        pass


class PrintHandler():

    def __init__(self, processors: dict[PrintProcessor]) -> None:
        self.processors = processors

    def print(self, printer: Printer, pdf: PdfReader):

        if pdf is None:
            raise MissingPDFException()

        if printer is None:
            raise PrinterIsEmptyException()

        if not self.processors:
            raise MissingProcessorException()

        path = pdf.stream.name

        for processor in self.processors:
            processor.print_page(
                printer=printer,
                path=path
            )


class PrinterIsEmptyException(BaseException):
    pass


class MissingPDFException(BaseException):
    pass


class MissingProcessorException(BaseException):
    pass
