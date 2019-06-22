__author__ = 'Tim Dilmaghani'
__date__ = '22.06.2019'

import os
import glob
import re
import pickle
from pathlib import Path
from subprocess import check_output

import cv2
import numpy as np
from PIL import Image, ImageDraw
from progressbar import progressbar

from page import Page
from processing import number_of_pages_in_pdf

class Document:
    '''
    Assumes path to a PDF (no OCR)
    '''
    def __init__(self, path_to_pdf: Path):
        self.path = path_to_pdf
        self.name = os.path.basename(self.path)
        self.num_pages = number_of_pages_in_pdf(self.path)
        self.pages = [Page(self.path, i) for i in range(1, self.num_pages)] # Need to start at 1 for pdftocairo

    def __repr__(self):
        return f'Document(name={self.name}, num_pages={self.num_pages}, path={self.path})'

    def __iter__(self):
        return iter(self.pages)

    def process(self):
        '''
        Starts to extract the structure of the document
        '''
        for page_object in progressbar(self.pages):
            page_object.process()
