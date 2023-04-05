import pytest

from bin.processing.payload_parser import PayloadParser, InvalidPayloadException, PrinterNotExistException
from bin.models.print_payload import PrintPayload

from bin.database.database import SessionLocal
from sqlalchemy.orm import Session as AlchemySession

from bin.database.models import Printer


@pytest.fixture
def parser():
    return PayloadParser()


@pytest.fixture()
def session() -> AlchemySession:
    return SessionLocal()


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    session = SessionLocal()
    session.query(Printer).delete()
    session.commit()


def test_parse_none_payload(parser: PayloadParser):
    with pytest.raises(InvalidPayloadException):
        parser.parse_payload(payload=None)


def test_parse_invalid_string_payload(parser: PayloadParser):
    with pytest.raises(InvalidPayloadException):
        parser.parse_payload(payload='')


def test_valid_payload_but_no_printer(parser: PayloadParser):
    with pytest.raises(PrinterNotExistException):
        parser.parse_payload(
            payload='{"base64":"1234","printer": "printer_1" ,"pages":[],"id":1}')


def test_valid_payload_but_wrong_printer(parser: PayloadParser, session: AlchemySession):
    printer = Printer(
        readable_name="Printer 2",
        progressor_identifier="printer_2",
        remote_identifier="printer_2"
    )
    session.add(printer)
    session.commit()

    with pytest.raises(PrinterNotExistException):
        parser.parse_payload(
            payload='{"base64":"1234","printer": "printer_1" ,"pages":[],"id":1}')


def test_valid_payload(parser: PayloadParser, session: AlchemySession):
    printer = Printer(
        readable_name="Printer 1",
        progressor_identifier="printer_1",
        remote_identifier="printer_1"
    )
    session.add(printer)
    session.commit()

    print_payload: PrintPayload = parser.parse_payload(
        payload='{"base64":"1234","printer": "printer_1" ,"pages":[],"id":1}')
    assert print_payload.base64 == "1234"
    assert print_payload.pages == []
    assert print_payload.printer.id == printer.id
    assert print_payload.identifier == 1


def test_valid_payload_multi_pages(parser: PayloadParser, session: AlchemySession):
    printer = Printer(
        readable_name="Printer 1",
        progressor_identifier="printer_1",
        remote_identifier="printer_1"
    )
    session.add(printer)
    session.commit()

    print_payload: PrintPayload = parser.parse_payload(
        payload='{"base64":"1234","printer": "printer_1" ,"pages":[1, 2],"id":1}')
    assert print_payload.base64 == "1234"
    assert print_payload.pages == [1, 2]
    assert print_payload.printer.id == printer.id
    assert print_payload.identifier == 1
