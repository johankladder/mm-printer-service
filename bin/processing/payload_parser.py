
import json

from sqlalchemy.orm import Session as AlchemySession
from bin.database.database import SessionLocal
from bin.models.print_payload import PrintPayload

from bin.database.models import Printer


class PayloadParser():

    def parse_payload(self, payload: str):
        if not payload:
            raise InvalidPayloadException()

        try:
            data = json.loads(payload)
        except:
            raise InvalidPayloadException()

        return self.__create_model_from_data(data)

    def __create_model_from_data(self, data: any):

        session: AlchemySession = SessionLocal()

        base_64 = data['base64']
        pages = data['pages']

        printer = session.query(Printer).filter(
            Printer.remote_identifier == data['printer']).first()

        if not printer:
            raise PrinterNotExistException()
        
        if not base_64:
            raise InvalidPayloadException()

        return PrintPayload(
            base64=base_64,
            printer=printer,
            pages=pages
        )


class InvalidPayloadException(BaseException):
    pass


class PrinterNotExistException(BaseException):
    pass