import matplotlib.pyplot as plt
import textwrap
import os

class Block:
    '''
    Represents an extracted block on a page
    in the pdf
    '''
    def __init__(self, i: int, block_img, block_text, x: int, y: int, w: int, h: int):
        self.id: int = i
        self.img = block_img
        self.x = w
        self.y = y
        self.w = w
        self.h = h
        self.area = h*w
        self.text = block_text
        self.type = None # table, text-block, heading, footer

    def __repr__(self):
        return f"Block(id={self.id}, text='{textwrap.shorten(self.text, width=30, placeholder='...')}',)"

    def save(self, path='./'):
        out_path = os.path.join(path, self.id + '.png')
        plt.imsave(out_path, self.img)

    def show(self):
        plt.imshow(self.img)
