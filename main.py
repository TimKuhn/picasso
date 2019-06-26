from picasso.document import Document
import os, sys

if __name__ == '__main__':
    path = input('\nPlease specify path to PDF: ')
    if os.path.isfile(path) and path.endswith('.pdf'):
        d = Document(path)
        d.process()
        print(d)
    else:
        print(path, 'is not a valid pdf file.')
        sys.exit()
     
