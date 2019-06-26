__author__ = 'Tim Dilmaghani'
__date__ = '22.06.2019'

import os
import glob
import re
import pickle
from pathlib import Path
from subprocess import check_output

import matplotlib.pyplot as plt
import textwrap
import cv2
import numpy as np
from PIL import Image, ImageDraw
from progressbar import progressbar
import seaborn as sns

#from picasso.page import Page
from picasso.processing import number_of_pages_in_pdf
from picasso.processing import draw_bounding_boxes_on_image
from picasso.processing import convert_to_image, translate_image_size_to_pdf_size
from picasso.processing import extract_block_coords_from_image
from picasso.processing import extract_block_image_from_coords
from picasso.processing import extract_block_text_from_coords


class Document:
    '''
    Assumes path to a PDF

    >>> document = Document('/path/to/pdf')
    >>> document.process() # runs the block extraction
    >>> document.pages[0] # to access single pages, or
    >>> document.pages[0].blocks[0] # to access block
    '''
    def __init__(self, path_to_pdf: Path):
        self.path = path_to_pdf
        self.name = os.path.basename(self.path)
        self.num_pages = number_of_pages_in_pdf(self.path)
        self.pages = [Page(self.path, i) for i in range(1, self.num_pages + 1)] # Need to start at 1 for pdftocairo
        self.ocr = False

    def __repr__(self):
        return f'Document(name={self.name}, num_pages={self.num_pages}, path={self.path}, ocr={self.ocr})'

    def __iter__(self):
        return iter(self.pages)

    def process(self, dilation_iterations: int = 6, ocr=False):
        '''
        Starts to extract the structure of the document
        '''
        self.ocr = ocr
        if self.ocr:
            # Load Module
            import pytesseract
            
        for page_object in progressbar(self.pages):
            page_object.process(dilation_iterations, self.ocr)

    def show_dist(self):
        '''
        Plots distribution of blocks in documents 
        this indicates whether you should adjust for the delation iteration
        '''
        x = [len(page.blocks) for page in self.pages]
        sns.distplot(x)


class Block:
    '''
    Represents an extracted block on a page
    in the pdf

    TODO: Need to understand where this block is within the page
    '''
    def __init__(self, i: int, block_img, block_text, x: int, y: int, w: int, h: int, page_img):
        self.id: int = i
        self.img = block_img
        self.img_page = page_img
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.area = h*w # TODO: Calculate normalized area (e.g. 30% of page)
        self.text = block_text
        self.type = None # table, text-block, heading, footer

    def __repr__(self):
        return f"Block(id={self.id}, type={self.type}, text='{textwrap.shorten(self.text, width=30, placeholder='...')}',)"

    def save(self, path='./'):
        out_path = os.path.join(path, self.id + '.png')
        plt.imsave(out_path, self.img)

    def show(self):
        plt.imshow(self.img)


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

    def process(self, dilation_iterations: int = 6, ocr=False):
        '''
        Starts the processing from pdf to image to blocks
        '''
        self.dilation_used = dilation_iterations

        # This is the heavy path. We make the image, extract blocks and text
        self.img = convert_to_image(self.path, self.page)
        self.ratio = translate_image_size_to_pdf_size(self.path, self.img, self.page)
        blocks_coords: list = extract_block_coords_from_image(self.img, dilation_iterations)
        blocks_images: list = extract_block_image_from_coords(self.img, blocks_coords)
        if ocr:
            blocks_text: list = [pytesseract.image_to_string(img) for img in blocks_images]
        else:
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

    def save(self, path='./'):
        out_path = os.path.join(path, self.id + '.png')
        plt.imsave(out_path, self.img)

    def show(self):
        '''
        Shows the original page as an image
        '''
        plt.imshow(self.img)

    def show_bounding_boxes(self):
        draw_bounding_boxes_on_image(self.img, self.blocks) 

