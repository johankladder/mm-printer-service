import pytest

from bin.processing.payload_parser import PayloadParser, InvalidPayloadException, PrinterNotExistException
from bin.models.print_payload import PrintPayload

@pytest.fixture
def parser():
    return PayloadParser()

def test_parse_none_payload(parser: PayloadParser):
    with pytest.raises(InvalidPayloadException):
        parser.parse_payload(payload=None)


def test_parse_invalid_string_payload(parser: PayloadParser):
    with pytest.raises(InvalidPayloadException):
        parser.parse_payload(payload='')

def test_valid_payload(parser: PayloadParser):
    print_payload: PrintPayload = parser.parse_payload(
        payload='{"base64":"1234","printer": "printer_1" ,"pages":[],"id":1}')
    assert print_payload.base64 == "1234"
    assert print_payload.pages == []
    assert print_payload.printer == "printer_1"
    assert print_payload.exclude == False


def test_valid_payload_multi_pages(parser: PayloadParser):
    print_payload: PrintPayload = parser.parse_payload(
        payload='{"base64":"1234","printer": "printer_1" ,"pages":[1, 2],"id":1}')
    assert print_payload.base64 == "1234"
    assert print_payload.pages == [1, 2]
    assert print_payload.printer == "printer_1"
    assert print_payload.exclude == False


def test_valid_payload_with_exclude(parser: PayloadParser):
    print_payload: PrintPayload = parser.parse_payload(
        payload='{"base64":"1234","printer": "printer_1" ,"pages":[],"id":1, "exclude": true}')
    assert print_payload.base64 == "1234"
    assert print_payload.pages == []
    assert print_payload.printer == "printer_1"
    assert print_payload.exclude == True


def test_valid_payload_with_url(parser: PayloadParser):
    print_payload: PrintPayload = parser.parse_payload(
        payload='{"url":"https://www.google.nl","printer": "printer_1" ,"pages":[],"id":1}')
    assert print_payload.url == "https://www.google.nl"
    assert print_payload.pages == []
    assert print_payload.printer == "printer_1"
    assert print_payload.exclude == False
