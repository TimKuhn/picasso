class Block:
    '''
    Represents an extracted block on a page
    in the pdf
    '''
    def __init__(self, i:int = 0, x: int, y: int, w: int, h: int):
        self.id = None # default 0 
        self.x = w
        self.y = y
        self.w = w
        self.h = h
        self.area = None
        self.text = None

    def save(self):
        pass

    def show(self):
        pass
