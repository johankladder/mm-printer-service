from base64 import b64decode
from pypdf import PdfReader
import tempfile
import requests
import os

from bin.models.print_payload import PrintPayload


class PDFGenerator():

    def generate(self, payload: PrintPayload) -> PdfReader:
        if not payload or (payload.base64 is None and payload.url is None):
            raise InvalidBase64Exception()

        if payload.base64:
            return PdfReader(self.__generate(base64=payload.base64))

        if payload.url:
            return PdfReader(self.__generate_url(url=payload.url))

    def __generate(self, base64: str):
        bytes = b64decode(base64, validate=True)
        if bytes[0:4] != b'%PDF':
            raise InvalidBase64Exception()

        fp = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        fp.write(bytes)
        return fp

    def __generate_url(self, url: str):
        response = requests.get(url)
        content_type = response.headers.get("Content-Type")
        if (response.status_code >= 200 and ('application/pdf' in content_type)):
            fp = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
            fp.write(response.content)
            return fp
        else:
            raise InvalidUrlException()


class InvalidBase64Exception(BaseException):
    pass


class InvalidUrlException(BaseException):
    pass
