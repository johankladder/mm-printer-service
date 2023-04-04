import pytest
import os

from pypdf import PdfReader

from bin.processing.merger import PDFMerger, InvalidPDFException, MergePagesOutOfBoundException, EmptyPDFException


@pytest.fixture
def merger():
    return PDFMerger()


@pytest.fixture
def pdf():
    path = os.path.join(os.path.dirname(__file__),
                        '../../resources/test-2-pages.pdf')
    return PdfReader(open(path, "rb"))


def test_merge_none_pdf(merger: PDFMerger):
    with pytest.raises(InvalidPDFException):
        merger.merge(pdf=None, pages=[])


def test_merge_pdf_out_of_bound_pages(merger: PDFMerger, pdf: PdfReader):
    with pytest.raises(MergePagesOutOfBoundException):
        merger.merge(pdf=pdf, pages=[3, 4])


def test_merge_pdf_underflow_pages(merger: PDFMerger, pdf: PdfReader):
    with pytest.raises(MergePagesOutOfBoundException):
        merger.merge(pdf=pdf, pages=[-1])


def test_merge_into_zero_page(merger: PDFMerger, pdf: PdfReader):
    with pytest.raises(EmptyPDFException):
        merger.merge(pdf=pdf, pages=[])


def test_merge_into_single_page(merger: PDFMerger, pdf: PdfReader):
    reader = merger.merge(pdf=pdf, pages=[0])
    assert len(reader.pages) == 1


def test_merge_into_multi_page(merger: PDFMerger, pdf: PdfReader):
    reader = merger.merge(pdf=pdf, pages=[0, 1])
    assert len(reader.pages) == 2
