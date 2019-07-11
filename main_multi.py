from picasso.document import Document
import multiprocessing
import time

from functools import wraps

def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print(f"@timefn: `{fn.__name__}` took {str(round(t2-t1, 2))} seconds")
        return result
    return measure_time


def timeit(i):
    start = time.time()

    d1 = Document('./data/beiersdorf_20184.pdf')
    d1.pages[5].process(3)

    end = time.time()
    print(f"Round: {i} Time: {round(end - start, 2)}")

def process():
    d1 = Document('./data/beiersdorf_20184.pdf')
    d1.pages[5].process(3)
    """
    for i in range(len(d1.pages)):
        print("====================================")
        d1.pages[i].process(3)
    """

if __name__ == '__main__':
    process()
