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

def draw_bounding_boxes_on_image(img, blocks: list):
    '''
    Draws bounding boxes on an image

    # TODO: DOES NOT WORK CORRECTLY
    '''
    
    img_c = img.copy()

    for block in blocks:
        x = block.x
        y = block.y
        w = block.w
        h = block.h
        # Draws the rectangles for presentation purposes, you can comment it out
        cv2.rectangle(img_c, (x,y), (x+w, y+h), (0,255,0), 1)
        
    return img_c


def number_of_pages_in_pdf(path) -> int:
    # Get number of pages of pdf
    try:
        pdf_info: str = str(check_output(['pdfinfo', path]))
        m = re.search('Pages:\s+(\d+)', pdf_info)
        return int(m.group(1))
    except:
        print(f'No number of pages found for `{path}`')
        return 0

def translate_image_size_to_pdf_size(path_to_pdf, img, page) -> float:
    '''
    Calculates ratio that is needed to translate between
    image size and pdf size. This is for example required 
    for text extraction with `pdftotext`

    returns: ratio 
    '''
    # Get y and x of the original image
    y_img, x_img, _ = img.shape

    # Get the layout of the PDF with pdfinfo
    out = check_output(["pdfinfo", "-rawdates", f"{path_to_pdf}"])
    matches = re.search('(\d+)\.\d+\sx\s(\d+)\.\d+', str(out))
    x_pdf = int(matches.group(1))
    y_pdf = int(matches.group(2))

    # Get the translation Ratio 
    return x_pdf/x_img

def extract_block_coords_from_image(img, dilation_iterations: int = 6) -> list:
    '''
    Takes an image, transforms and pre-processes it
    and returns identified blocks
    '''

    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Edge Detection
    edges = cv2.Canny(img_gray, 100, 200)
    kernel = np.ones((5,5), np.float32)/25
    ret, mask = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY)

    # Dilutes the image, which is key to finding rectangulars
    # iterations between 3 and 6 seem to work pretty good - the higher, the fewer blocks you get
    dilation = cv2.dilate(mask, kernel, iterations=dilation_iterations)

    # Finds the rectangulars in the image
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Approximated rectangular areas are used to extract image area (blob)
    blocks = []
    for i, c in enumerate(contours):
        # Extract area and a rectangular
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)

        # Construct a Block Object from the image block and the coords
        #img_block = img[y:y + h, x:x + w]
        #blocks.append((img_block, x, y, w, h))
        
        blocks.append((x,y,w,h))

    return blocks[::-1] # reverse order


          
def extract_block_image_from_coords(img, coords: tuple) -> list:
    '''
    Extract the block specified in coords from the image
    '''

    image_blocks = []
    for i, coord in enumerate(coords):
        x, y, w, h = coord
        image_block = img[y:y + h, x:x + w]
        image_blocks.append(image_block)

    return image_blocks

def extract_block_text_from_coords(path_to_pdf, page: int, coords: tuple, r: float) -> list:
    """
    Takes a blob which consists of 4 coordinates (x,y,h,w)
    it also takes the translation ratio 'r' that is required
    to translate the coordinates from the image to the pdf

    Then pdftotext takes the coordinates to extract the text 
    from the area

    Returns: str: blob_text
    """

    blocks_text = []
    for coord in coords:
        # Extract block coordinates
        x,y,w,h = coord

        # Translated coordinates
        x_new, y_new, w_new, h_new = int(x*r) ,int(y*r), int(w*r), int(h*r) 

        # Use Pdftotext to get blobs
        os.system(f"pdftotext -layout -l {page} -f {page} -x {x_new} -y {y_new} -W {w_new} -H {h_new} {path_to_pdf} ./tmp.txt")
        with open('./tmp.txt', "r") as f:
            block_text = f.read()

        os.remove('./tmp.txt')

        blocks_text.append(block_text)

    return blocks_text
