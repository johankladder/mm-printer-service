from pypdf import PdfReader
from bin.models.print_payload import PrintPayload

from paho.mqtt.client import Client


class PrintProcessor():

    def __init__(self, client: Client = None) -> None:
        self.client = client

    def print_page(self, print_payload: PrintPayload, path: str):
        pass


class PrintHandler():

    def __init__(self, processors: dict[PrintProcessor]) -> None:
        self.processors = processors

    def print(self, print_payload: PrintPayload, pdf: PdfReader):

        if pdf is None:
            raise MissingPDFException()

        if print_payload.printer is None:
            raise PrinterIsEmptyException()

        if not self.processors:
            raise MissingProcessorException()

        path = pdf.stream.name

        for processor in self.processors:
            print("Print page with processor: ", processor)
            processor.print_page(
                print_payload=print_payload,
                path=path
            )


class PrinterIsEmptyException(BaseException):
    pass


class MissingPDFException(BaseException):
    pass


class MissingProcessorException(BaseException):
    pass
