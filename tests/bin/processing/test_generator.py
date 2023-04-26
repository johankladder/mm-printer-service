import pytest
import os

from bin.processing.generator import PDFGenerator, InvalidBase64Exception, InvalidUrlException
from bin.models.print_payload import PrintPayload


@pytest.fixture
def generator():
    return PDFGenerator()


@pytest.fixture
def payload():
    return PrintPayload(
        printer=1,
        pages=[]
    )


def test_generating_none_payload(generator: PDFGenerator):
    with pytest.raises(InvalidBase64Exception):
        generator.generate(payload=None)


def test_generating_invalid_base64(generator: PDFGenerator, payload: PrintPayload):
    payload.base64 = "eefe0ffefefefefe8efe8fe8"
    with pytest.raises(InvalidBase64Exception):
        generator.generate(
            payload=payload
        )


def test_generating_invalid_url(generator: PDFGenerator, payload: PrintPayload):
    payload.url = "https://www.google.nl"
    with pytest.raises(InvalidUrlException):
        generator.generate(
            payload=payload
        )


def test_generating_not_accesable_url(generator: PDFGenerator, payload: PrintPayload):
    payload.url = "https://www.google.nl/test.pdf"
    with pytest.raises(InvalidUrlException):
        generator.generate(
            payload=payload
        )


def test_generating_with_valid_url(generator: PDFGenerator, payload: PrintPayload):
    payload.url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    reader = generator.generate(
        payload=payload
    )
    assert len(reader.pages) == 1

def test_generating_with_valid_url_with_options(generator: PDFGenerator, payload: PrintPayload):
    payload.url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf?any"
    reader = generator.generate(
        payload=payload
    )
    assert len(reader.pages) == 1

def test_generating_with_valid_base64(generator: PDFGenerator, payload: PrintPayload):
    path = os.path.join(os.path.dirname(__file__),
                        '../../resources/test-2-pages-base64.txt')

    with open(path, 'r') as file:
        base64 = file.read().replace('\n', '')
        payload.base64 = base64

        reader = generator.generate(payload=payload)
        assert len(reader.pages) == 2
