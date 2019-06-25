import pytest

from reportlab.pdfgen import canvas
from picasso.page import Page

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
