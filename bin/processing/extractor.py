import os
from pypdf import PdfReader

class PDFExtractor():

    def extract(self, path: str):
        if path is None or os.path.isfile(path) is False:
            raise InvalidPDFPathException()

        _, extension = os.path.splitext(path)
        if extension != '.pdf':
            raise FileNotPDFException()

        return self.__create_model_from_file(path)

    def __create_model_from_file(self, path: str) -> PdfReader:
        return PdfReader(open(path, "rb"))


class InvalidPDFPathException(BaseException):
    pass


class FileNotPDFException(BaseException):
    pass
