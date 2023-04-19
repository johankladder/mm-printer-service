
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
        base_64 = data.get('base64', None)
        pages = data['pages']
        printer = data['printer']
        exclude = data.get('exclude', False)
        url = data.get('url', None)

        if not printer:
            raise PrinterNotExistException()

        if not base_64 and not url:
            raise InvalidPayloadException()

        return PrintPayload(
            base64=base_64,
            printer=printer,
            pages=pages,
            exclude=exclude,
            url=url
        )


class InvalidPayloadException(BaseException):
    pass


class PrinterNotExistException(BaseException):
    pass
