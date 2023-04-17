
import json

from bin.models.print_payload import PrintPayload

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
        base_64 = data['base64']
        pages = data['pages']
        printer = data['printer']
        exclude = data.get('exclude', False)

        if not printer:
            raise PrinterNotExistException()
        
        if not base_64:
            raise InvalidPayloadException()

        return PrintPayload(
            base64=base_64,
            printer=printer,
            pages=pages,
            exclude=exclude
        )


class InvalidPayloadException(BaseException):
    pass


class PrinterNotExistException(BaseException):
    pass