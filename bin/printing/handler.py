from pypdf import PdfReader


class PrintProcessor():

    def print_page(self, printer: any, path: str):
        pass


class PrintHandler():

    def __init__(self, processor: PrintProcessor) -> None:
        self.processor = processor

    def print(self, printer, pdf: PdfReader):

        if pdf is None:
            raise MissingPDFException()

        if printer is None:
            raise PrinterIsEmptyException()

        if self.processor is None:
            raise MissingProcessorException()

        path = pdf.stream.name
        self.processor.print_page(
            printer=printer,
            path=path
        )


class PrinterIsEmptyException(BaseException):
    pass


class MissingPDFException(BaseException):
    pass


class MissingProcessorException(BaseException):
    pass
