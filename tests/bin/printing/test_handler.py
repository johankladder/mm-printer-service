import pytest
import os

from unittest.mock import MagicMock

from pypdf import PdfReader
from bin.printing.handler import PrintHandler, PrintProcessor, PrinterIsEmptyException, MissingPDFException, MissingProcessorException

from bin.models.print_payload import PrintPayload


@pytest.fixture
def processor():
    processor = PrintProcessor()
    processor.print_page = MagicMock()
    return processor


@pytest.fixture
def handler(processor: PrintProcessor):
    return PrintHandler(
        processors=[processor]
    )


@pytest.fixture
def pdf():
    path = os.path.join(os.path.dirname(__file__),
                        '../../resources/test-2-pages.pdf')
    return PdfReader(open(path, "rb"))


def test_print_with_empty_printer(handler: PrintHandler, pdf: PdfReader):
    with pytest.raises(PrinterIsEmptyException):
        handler.print(print_payload=None, pdf=pdf)


def test_print_with_empty_printer(handler: PrintHandler):
    with pytest.raises(MissingPDFException):
        handler.print(print_payload=1, pdf=None)


def test_print_without_processor(handler: PrintHandler, pdf: PdfReader):
    with pytest.raises(MissingProcessorException):
        handler.processors = None
        handler.print(print_payload=PrintPayload(
            printer=1,
            base64='1234',
            pages=[]
        ), pdf=pdf)


def test_print_happy_flow(handler: PrintHandler, pdf: PdfReader):
    handler.print(print_payload=PrintPayload(
        printer=1,
        base64='1234',
        pages=[]
    ), pdf=pdf)
    handler.processors[0].print_page.assert_called()
