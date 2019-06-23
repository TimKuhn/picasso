from pathlib import Path
import os
import matplotlib.pyplot as plt

from block import Block
from processing import draw_bounding_boxes_on_image
from processing import convert_to_image, translate_image_size_to_pdf_size
from processing import extract_block_coords_from_image
from processing import extract_block_image_from_coords
from processing import extract_block_text_from_coords

class Page:
    '''
    Page Element
    '''
    def __init__(self, path_to_pdf: Path, page: int):
        self.id: int = os.path.basename(path_to_pdf) + f'_page_{page}'
        self.page: int = page
        self.path: Path = path_to_pdf 
        self.ratio = None
        self.blocks: list = []
        self.img = None # Numpy array
        self.dilation_used = None

    def __iter__(self):
        return iter(self.blocks)

    def __repr__(self):
        return f'Page(id={self.id}, page={self.page}, blocks={len(self.blocks)})'

    def process(self, dilation_iterations: int = 6):
        '''
        Starts the processing from pdf to image to blocks
        '''
        self.dilation_used = dilation_iterations

        # This is the heavy path. We make the image, extract blocks and text
        self.img = convert_to_image(self.path, self.page)
        self.ratio = translate_image_size_to_pdf_size(self.path, self.img, self.page)
        blocks_coords: list = extract_block_coords_from_image(self.img, dilation_iterations)
        blocks_images: list = extract_block_image_from_coords(self.img, blocks_coords)
        blocks_text: list = extract_block_text_from_coords(self.path, self.page, blocks_coords, self.ratio)

        # Create Block instances based on the previously extracted info
        cnt = 0
        self.blocks = [] # If process is called again, we want an empty list
        for img, text, coords in zip(blocks_images, blocks_text, blocks_coords):
            x,y,w,h = coords
            block_id = self.id + f'_block_{cnt}'
            img_page = self.img
            b = Block(block_id, img, text, x, y, w, h, img_page)
            self.blocks.append(b)
            cnt += 1

    def save(self):
        plt.imsave(self.id + '.png', self.img)

    def show(self):
        '''
        Shows the original page as an image
        '''
        plt.imshow(self.img)

    def show_bounding_boxes(self):
        draw_bounding_boxes_on_image(self.img, self.blocks) 
