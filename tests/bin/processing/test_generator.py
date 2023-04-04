import pytest
import os

from bin.processing.generator import PDFGenerator, InvalidBase64Exception

@pytest.fixture
def generator():
    return PDFGenerator()

def test_generating_none_str(generator: PDFGenerator):
    with pytest.raises(InvalidBase64Exception):
        generator.generate(base64=None)

def test_generating_invalid_base64(generator: PDFGenerator):
    with pytest.raises(InvalidBase64Exception):
        generator.generate(base64="eefe0ffefefefefe8efe8fe8")


def test_generating_with_valid_base64(generator: PDFGenerator):
    path = os.path.join(os.path.dirname(__file__),
                        '../../resources/test-2-pages-base64.txt')
    
    with open(path, 'r') as file:
        base64 = file.read().replace('\n', '')
        reader = generator.generate(base64=base64)
        assert len(reader.pages) == 2
