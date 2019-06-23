from document import Document
from line_detection import Lines
import pdb

import matplotlib.pyplot as plt
import cv2
import pickle          

if __name__ == '__main__':
    path = '../data/bmw_20181.pdf'
    test_page = 12
    d = Document(path)
    print(d)
    d.pages[test_page].process()
    table = d.pages[test_page].blocks[8].img
    #table_img = cv2.imread('./table.png')


    # Load sample table
    #with open('table.png', 'rb') as f:
    #    table = pickle.load(f)
 
    lines = Lines(table)

    
    #pdb.set_trace()
    lines.find_lines()

