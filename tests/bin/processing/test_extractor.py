import pytest
import os
from bin.processing.extractor import PDFExtractor, InvalidPDFPathException, FileNotPDFException


@pytest.fixture
def extractor():
    return PDFExtractor()


def test_extracting_none_path(extractor: PDFExtractor):
    with pytest.raises(InvalidPDFPathException):
        extractor.extract(path=None)


def test_extracting_invalid_path(extractor: PDFExtractor):
    with pytest.raises(InvalidPDFPathException):
        extractor.extract(path='/invalid')


def test_extracting_invalid_extension(extractor: PDFExtractor):
    with pytest.raises(FileNotPDFException):
        path = os.path.join(os.path.dirname(__file__),
                            '../../resources/invalid-pdf.png')
        extractor.extract(path=path)


def test_extracting_valid_pdf(extractor: PDFExtractor):
    path = os.path.join(os.path.dirname(__file__),
                        '../../resources/test-2-pages.pdf')
    reader = extractor.extract(path=path)
    assert len(reader.pages) == 2
