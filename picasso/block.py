import matplotlib.pyplot as plt
import textwrap

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
        return f"Block(id={self.id}, x={self.x}, y={self.y}, w={self.w}, h={self.h}, area={self.area}, text='{textwrap.shorten(self.text, width=30, placeholder='...')}',)"

    def save(self):
        plt.imsave(self.id + '.png', self.img)

    def show(self):
        plt.imshow(self.img)
