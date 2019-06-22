import os
import glob
from subprocess import check_output
import re

import cv2
import numpy as np

from block import Block

def convert_to_image(path, page):
    '''
    Converts a PDF page to png image
    Saves the temporary image on disk, then
    loads and returns the file. 
    Finally tmp image is deleted from disk
    '''

    # Converts a pdf page to an image with 'pdftocairo' and saves file as a tmp
    output_type = 'png'
    resolution = 150
    output_path = './tmp' # Save to current directory, will be deleted later
    
    # External linux command
    os.system(f'pdftocairo -{output_type} -r {resolution} -f {page} -l {page} {path} {output_path}')

    # the name we give `tmp` is appended by the page, so the name is unclear
    img_path = glob.glob('tmp*.png')[0] 
    img_color = cv2.imread(img_path)

    # Delete the tmp image from disk
    os.remove(img_path)

    return img_color

def number_of_pages_in_pdf(path) -> int:
    # Get number of pages of pdf
    try:
        pdf_info: str = str(check_output(['pdfinfo', path]))
        m = re.search('Pages:\s+(\d+)', pdf_info)
        return int(m.group(1))
    except:
        print(f'No number of pages found for `{path}`')
        return 0

def extract_blocks_from_image(img, dilation_iterations: int = 6) -> [Block]:
    '''
    Takes an image, transforms and pre-processes it
    and returns identified blocks
    '''

    # Edge Detection
    edges = cv2.Canny(img, 100, 200)
    kernel = np.ones((5,5), np.float32)/25
    ret, mask = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY)

    # Dilutes the image, which is key to finding rectangulars
    # iterations between 3 and 6 seem to work pretty good - the higher, the fewer blocks you get
    dilation = cv2.dilate(mask, kernel, iterations=dilation_iterations)

    # Finds the rectangulars in the image
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Approximated rectangular areas are used to extract image area (blob)
    img_blocks = []
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)
        img_blocks.append((x,y,w,h))
                        
        # Draws the rectangles for presentation purposes, you can comment it out
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 1)
                                    
    img_blocks = img_blocks[::-1] # Blobs are stored in wrong order
                                        
    print(f"Number of Blobs detected =>", len(img_blocks))

    return img_blocks







