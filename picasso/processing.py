import os, sys
import glob
from subprocess import check_output
import re
import uuid

import matplotlib.pyplot as plt
import cv2
import numpy as np

from PIL import Image

#####################
#                   #
#    Utilities      #
#                   #
#####################
from functools import wraps
import time
def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print(f"@timfn: {str(round(t2-t1, 1))} secs -> {fn.__name__}")
        return result
    return measure_time


@timefn
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
    unique_out_path = str(uuid.uuid4())
    
    # External linux command
    cmd = f"pdftocairo -q -{output_type} -r {resolution} -f {page} -l {page} '{path}' {unique_out_path}"
    os.system(cmd)

    # the name we give `tmp` is appended by the page number, so the name is unclear because sometimes it is 001 or 01  depending on the file
    img_path = glob.glob(f'{unique_out_path}*.png')[0] 
    img_color = cv2.imread(img_path)

    # Delete the tmp image from disk
    os.remove(img_path)

    return img_color

@timefn
def draw_bounding_boxes_on_image(img, blocks: list):
    '''
    Draws bounding boxes on an image
    '''
    img_c = img.copy()
    for block in blocks:
        x = block.x
        y = block.y
        w = block.w
        h = block.h
        cv2.rectangle(img_c, (x,y), (x+w, y+h), (0,0,255), 2)
        
    return img_c

@timefn
def number_of_pages_in_pdf(path) -> int:
    # Get number of pages of pdf
    try:
        pdf_info: str = str(check_output(['pdfinfo', path]))
        m = re.search('Pages:\s+(\d+)', pdf_info)
        return int(m.group(1))
    except:
        print(f'No number of pages found for `{path}`')
        return 0

@timefn
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
    matches = re.search('(\d+)(\.\d+)?\s+x\s+(\d+)(\.\d+)?', str(out))
    if matches:
        x_pdf = int(matches.group(1))
        y_pdf = int(matches.group(3))

        # Get the translation Ratio 
        return x_pdf/x_img

    else:
        print('ERROR: cannot find size of pdf page -> EXITING')
        sys.exit()

@timefn
def extract_block_coords_from_image(img, dilation_iterations: int = 3) -> list:
    '''
    Takes an image, transforms and pre-processes it
    and returns identified blocks
    '''

    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Edge Detection
    edges = cv2.Canny(img_gray, 100, 200)
    kernel = np.ones((6,6), np.float32)/25
    ret, mask = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY)

    # Dilutes the image, which is key to finding rectangulars
    # iterations between 3 and 6 seem to work pretty good - the higher, the fewer blocks you get
    dilation = cv2.dilate(mask, kernel, iterations=dilation_iterations)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
    closing_copy = closing.copy()

    # Finds the rectangulars in the image
    contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Approximated rectangular areas are used to extract image area (blob)
    blocks = []
    for i, c in enumerate(contours):
        # Extract area and a rectangular
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)
       
        blocks.append((x,y,w,h))

    blocks_reversed = blocks[::-1] # reverse order

    return (blocks_reversed, closing_copy)

@timefn
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

@timefn
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
        unique_out_path = str(uuid.uuid4()) + '.txt'
        cmd = f"pdftotext -q -enc 'UTF-8' -layout -l {page} -f {page} -x {x_new} -y {y_new} -W {w_new} -H {h_new} '{path_to_pdf}' {unique_out_path}"
        os.system(cmd)

        # pdftotext writes temporary file to disk and we read the input in
        with open(unique_out_path, "r") as f:
            block_text = f.read()

        # Delete the temp file
        os.remove(unique_out_path)

        blocks_text.append(block_text)

    return blocks_text
