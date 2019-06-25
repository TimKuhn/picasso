import pytest
import os
from picasso.document import Document
from reportlab.pdfgen import canvas


class TestDocument(object):
    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        # Fake PDF
        cls.path = '/tmp/test.pdf'
        c = canvas.Canvas(cls.path)
        # Creates 1 Page and 1 Block
        c.drawString(100, 750, f'This is a test block that\nI want to parse!!!')
        c.save()
        
        # Document processing
        cls.d = Document(cls.path)
        cls.d.process()

    def test_document_returns_one_page(self):
        assert len(self.d.pages) == 1

    def test_document_returns_one_block(self):
        assert len(self.d.pages[0].blocks) == 1

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        # Remove the fake PDF
        try:
            os.remove('/tmp/test.pdf')
        except:
            pass
