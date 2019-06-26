from itertools import product, tee
from pygame import Rect

def block_overlaps(block1, block2) -> bool:
    '''
    Assumes two block objects and returns True if
    they overlap and False otherwise
    '''
    rect1 = Rect(block1.x, block1.y, block1.w, block1.h)
    rect2 = Rect(block2.x, block2.y, block2.w, block2.h)
    return rect1.colliderect(rect2)




#############################################
#                                           #
#           Can it be deleted???            #
#                                           #
#############################################

def test():
    print('\nExample 1:')
    a = Rectangle(1, 1, 5, 5)
    b = Rectangle(3, 3, 7, 7)
    print(a & b)
    print(list(a - b))
    ##########################
    print('\nExample 2:')
    b = Rectangle(3, 2, 7, 4)
    print(a & b)
    print(list(a - b))
    ##########################
    print('\nExample 3:')
    b = Rectangle(2, 2, 4, 4)
    print(a & b)
    print(list(a - b))
    ##########################
    print('\nExample 4:')
    b = Rectangle(6, 2, 10, 6)
    print(a & b)
    print(list(a - b))
    ##########################
    print('\nExample 5:')
    b = Rectangle(0, 0, 6, 6)
    print(a & b)
    print(list(a - b))
    ##########################
    print('\nExample6:')
    b =Rectangle(2,0,4,6)
    print(a&b)
    print(list(a - b))

def pairwise(iterable):
    "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)




class Rectangle_OLD:
    __slots__ = '__x1', '__y1', '__x2', '__y2'

    def __init__(self, x1, y1, x2, y2):
        self.__setstate__((min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, ', '.join(map(repr, self)))

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return self.data != other.data

    def __hash__(self):
        return hash(self.data)

    def __len__(self):
        return 4

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __and__(self, other):
        x1, y1, x2, y2 = max(self.x1, other.x1), max(self.y1, other.y1), \
                         min(self.x2, other.x2), min(self.y2, other.y2)

        if x1 < x2 and y1 < y2:
            return type(self)(x1, y1, x2, y2)

    def __sub__(self, other):
        intersection = self & other
        if intersection is None:
            yield self
        else:
            x, y = {self.x1, self.x2}, {self.y1, self.y2}
            if self.x1 < other.x1 < self.x2:
                x.add(other.x1)
            if self.y1 < other.y1 < self.y2:
                y.add(other.y1)
            if self.x1 < other.x2 < self.x2:
                x.add(other.x2)
            if self.y1 < other.y2 < self.y2:
                y.add(other.y2)
            for (x1, x2), (y1, y2) in product(pairwise(sorted(x)),
                                              pairwise(sorted(y))):
                instance = type(self)(x1, y1, x2, y2)
                if instance != intersection:
                    yield instance

    def __getstate__(self):
        return self.x1, self.y1, self.x2, self.y2

    def __setstate__(self, state):
        self.__x1, self.__y1, self.__x2, self.__y2 = state

    @property
    def x1(self):
        return self.__x1

    @property
    def x2(self):
        return self.__x2

    @property
    def y1(self):
        return self.__y1

    @property
    def y2(self):
        return self.__y2

    intersection = __and__

    difference = __sub__
    data = property(__getstate__)

if __name__ == '__main__':
    test()



















































