from base64 import b64decode
from pypdf import PdfReader
import tempfile


class PDFGenerator():

    def generate(self, base64: str) -> PdfReader:
        if base64 is None:
            raise InvalidBase64Exception()

        bytes = b64decode(base64, validate=True)
        if bytes[0:4] != b'%PDF':
            raise InvalidBase64Exception()

        fp = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        fp.write(bytes)

        return PdfReader(fp)


class InvalidBase64Exception(BaseException):
    pass
