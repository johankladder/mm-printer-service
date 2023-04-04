import pytest

from bin.database.database import SessionLocal
from sqlalchemy.orm import Session as AlchemySession

from bin.database.models import Printer


@pytest.fixture()
def session() -> AlchemySession:
    return SessionLocal()


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    session = SessionLocal()
    session.query(Printer).delete()
    session.commit()


def test_printer(session: AlchemySession):
    printer = Printer(
        readable_name="Printer 1",
        progressor_identifier="printer_1",
        remote_identifier="printer_1"
    )
    session.add(printer)
    session.commit()

    assert len(session.query(Printer).all()) == 1
