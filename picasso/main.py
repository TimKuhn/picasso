from document import Document
from line_detection import Lines
import pdb
import glob
import matplotlib.pyplot as plt
import cv2
import pickle          

if __name__ == '__main__':
    path = glob.glob('../data/scan*')[0]
    d = Document(path)
    
    #pdb.set_trace()
    d.process(ocr=True)

     
