import pytest
import os
from picasso.document import Document, Page, Block
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
        cls.text = f'This is a test block that\nI want to parse!!!'
        c.drawString(100, 750, cls.text)
        c.save()
        
        # Document processing
        cls.d = Document(cls.path)
        cls.d.process()

    def test_document_returns_one_page(self):
        assert len(self.d.pages) == 1

    def test_document_returns_one_block(self):
        assert len(self.d.pages[0].blocks) == 1

    def test_document_block_has_text_parsed(self):
        """
        Parsing might contain special characters that are not 
        correctly encoded. Therefore, it might produce more text than 
        initially stored in text variable.
        """
        assert len(self.d.pages[0].blocks[0].text) >= len(self.text)

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

class TestPage(object):
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
 
        cls.p = Page(cls.path, 1) # page starts at 1 not at 0

    def test_page_has_correct_id(self):
        assert self.p.id == 'test.pdf_page_1'
