class Block:
    '''
    Represents an extracted block on a page
    in the pdf
    '''
    def __init__(self, i: int, img_block, x: int, y: int, w: int, h: int):
        self.id: int = i
        self.img = img_block
        self.x = w
        self.y = y
        self.w = w
        self.h = h
        self.area = h*w
        self.text = ''

    def __repr__(self):
        return f"Block(id={self.id}, text='{self.text}', area={self.area})"

    def save(self):
        pass

    def show(self):
        pass
