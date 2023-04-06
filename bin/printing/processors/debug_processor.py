
from bin.printing.handler import PrintProcessor
from bin.models.print_payload import PrintPayload
from bin.processing.extractor import PDFExtractor

class DebugProcessor(PrintProcessor):

    def print_page(self, print_payload: PrintPayload, path: str):
        pdf = PDFExtractor().extract(path)

        print("DEBUG: Print path: %s" % (path))
        print("DEBUG: Printing on printer: %s" %
              (print_payload.printer.progressor_identifier))
        print("DEBUG: Printing: %i pages" % (len(pdf.pages)))
