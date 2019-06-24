'''
Annotation for image classification
First, create a document object and feed that into
the annotation tool
'''


import tkinter as tk
import glob
from PIL import Image
import random
#from document import Document

CLASSES = {
        1:"Table", 
        2:"Non-Table",
        }

HEIGHT = 600
WIDTH = 2500

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

def callback(button):
    print(button)
    class_selected = button['text']
    # new image

    i = random.randint(0, 5)
    path = glob.glob('../data/train/table/*.png')[i]
    img2 = tk.PhotoImage(file=path)
    image_l.configure(image=img2)
    image_l.image = img2
    
        

# Table Button
t = tk.Button(text="Table", height=10, width=20, background='blue', foreground="white", command=lambda: callback(t))
t.pack()
root.bind("1", callback)

# Non-table Button
nont = tk.Button(text="Non-Table", height=10, width=20, background='green', foreground="white", command=lambda: callback(nont))
nont.pack()

blob = glob.glob('./*.png')[0]
image_t = tk.PhotoImage(file=blob)
image_l = tk.Label(root, image=image_t)
image_l.place(x=0, y=0, relwidth=0.5, relheight=0.5)


frame = tk.Frame(root, bg='#80c1ff')
frame.pack()

# QUIT Button
quit = tk.Button(text="Quit", background="red", command=root.destroy)
quit.pack()

root.bind("<Return>", callback)
root.mainloop()
