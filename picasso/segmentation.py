'''
Implements several algorithms to detect different types 
of blocks in the document. These types might be 

- Text Blocks
- Tables
- Table Introduction
- Table Header Row
- Footnotes
- Page Number
- Title
- Header
- Subheader
- Signature
- more...

'''
from page import Page
from block import Block

class Segmentation:
    '''
    Interface that implements different
    algorithms to classify blocks in a page
    into different types
    '''

    def __init__(self):
        pass

    def classify_page(self, page: Page):
        '''
        Runs different algorithms on the image 
        and tries to detect one of several classes
        '''
        for block in page:
            self.classify_block(block)
        
    def classify_block(self, block: Block):
        '''
        Writes the class to the block instance
        '''
        if len(block.text) > 100:
            block.type = 'text'
        else:
            block.type = 'table'
 

