
from bin.printing.handler import PrintProcessor
from bin.database.models import Printer

from pypdf import PdfReader

from bin.processing.extractor import PDFExtractor


class DebugProcessor(PrintProcessor):

    def print_page(self, printer: Printer, path: str):
        pdf = PDFExtractor().extract(path)

        print("DEBUG: Print path: %s" % (path))
        print("DEBUG: Printing on printer: %s" % (printer.progressor_identifier))
        print("DEBUG: Printing: %i pages" % (len(pdf.pages)))
