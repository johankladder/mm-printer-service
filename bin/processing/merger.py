from pypdf import PdfReader, PdfWriter
import tempfile


class PDFMerger():

    def merge(self, pdf: PdfReader, pages: dict[int]) -> PdfReader:
        if pdf is None:
            raise InvalidPDFException

        if len(pages) == 0:
            raise EmptyPDFException()

        total_pages = len(pdf.pages)
        if not all(value < total_pages and value >= 0 for value in pages):
            raise MergePagesOutOfBoundException

        writer = PdfWriter()
        for page in pages:
            writer.add_page(pdf.pages[page])

        fp = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        writer.write(fp)

        return PdfReader(fp)


class InvalidPDFException(BaseException):
    pass


class MergePagesOutOfBoundException(BaseException):
    pass


class EmptyPDFException(BaseException):
    pass
