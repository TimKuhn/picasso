import matplotlib.pyplot as plt
import textwrap
import os

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
        self.x = w
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
