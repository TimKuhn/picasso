from pathlib import Path
import os

from processing import convert_to_image, extract_blocks_from_image

class Page:
    '''
    Page Element that holds Blocks
    '''
    def __init__(self, path_to_pdf: Path, page: int):
        self.id: int = os.path.basename(path_to_pdf) + f'_page_{page}'
        self.page: int = page
        self.path: Path = path_to_pdf 
        self.blocks: list = []
        self.img = None

    def __repr__(self):
        return f'Page(id={self.id}, page={self.page}, blocks={len(self.blocks)})'

    def process(self, dilation_iterations: int = 6):
        '''
        Starts the processing from pdf to image to blocks
        '''
        self.img = convert_to_image(self.path, self.page)
        self.blocks = extract_blocks_from_image(self.img, dilation_iterations)

    def show_original(self):
        '''
        Shows the original page as an image
        '''
        pass

    
