import pytest
from pytest_mock import mocker
import os
from picasso.document import Document, Page, Block
from reportlab.pdfgen import canvas
import numpy as np


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


class TestBlock(object):
    """
    def test_block_collides(self, mocker):
        '''
        Should return true for the two blocks specified in this 
        function.
        '''
        # Patching a function that requires a real image
        mocker.patch.object(Block, '_normalized_area')
        Block._normalized_area.return_value = 0.53

        b1 = Block(i=1,block_img=1,block_text="",x=154,y=82,w=1041,h=396,page_img=1)
        b2 = Block(i=2,block_img=1,block_text="",x=152,y=358,w=469,h=170,page_img=1)
        
        assert b1.collides_with(b2) == True
    """




