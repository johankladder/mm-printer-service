from pypdf import PdfReader, PdfWriter
import tempfile


class PDFMerger():

    def merge(self, pdf: PdfReader, pages: dict[int], exclude: bool = False) -> PdfReader:
        if pdf is None:
            raise InvalidPDFException

        total_pages = len(pdf.pages)
        if not all(value < total_pages and value >= 0 for value in pages):
            raise MergePagesOutOfBoundException

        if (not exclude and len(pages) == 0) or (exclude == True and len(pages) >= total_pages):
            raise EmptyPDFException()

        writer = PdfWriter()

        if not exclude:
            for page in pages:
                writer.add_page(pdf.pages[page])
        else:
            for index, page in enumerate(pdf.pages):
                if index not in pages:
                    writer.add_page(pdf.pages[index])

        fp = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        writer.write(fp)

        return PdfReader(fp)


class InvalidPDFException(BaseException):
    pass


class MergePagesOutOfBoundException(BaseException):
    pass


class EmptyPDFException(BaseException):
    pass
