from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk


def to16(x):
    x = hex(x)[2:]
    if len(x) == 1:
        x = '0'+x
    return(x)

def get_color(c):
    color = '#'+to16(c[0])+to16(c[1])+to16(c[2])
    return(color)


def init_centroid(im, imheight, imwidth):
    n = imheight*imwidth
    cs = set()
    print(n)
    c3, c5 = (256, 256, 256), (256, 256, 256)
    c4, c6 = (-1, -1, -1), (-1, -1, -1)

    r = [x for x in im.getdata()]
    r.sort(key = lambda param: param[0])
    c1 = r[0]
    c2 = r[n-1]
    cs.add(c1)
    cs.add(c2)

    for (r, g, b) in im.getdata():
        if (r, g, b) not in cs:
            if g<c3[1]:
                c3 = (r, g, b)
    cs.add(c3)
    
    for (r, g, b) in im.getdata():
        if (r, g, b) not in cs:
            if g>c4[1]:
                c4 = (r, g, b)
    cs.add(c4)
    
    for (r, g, b) in im.getdata():
        if (r, g, b) not in cs:
            if b<c5[2]:
                c5 = (r, g, b)
    cs.add(c5)
    
    for (r, g, b) in im.getdata():
        if (r, g, b) not in cs:
            if b>c6[2]:
                c6 = (r, g, b)

    cs.add(c6)
    print(cs)
    return(c1, c2, c3, c4, c5)


def get_distance(r, g, b, c):
    return (((r-c[0])**2+(g-c[1])**2+(b-c[2])**2)**(1/2))


def get_clasters(im, c1, c2, c3, c4, c5, cl1, cl2, cl3, cl4, cl5, status):
    clasters = [[], [], [], [], []]
    for (r, g, b) in im.getdata():
        i = 0
        min_distance = (1000000, 0)
        for c in c1, c2, c3, c4, c5:
            distance = (get_distance(r, g, b, c), i)
            if distance[0] < min_distance[0]:
                min_distance = distance
            i += 1
        clasters[min_distance[1]].append((r, g, b))            
    if clasters[0] == cl1 and clasters[1] == cl2 and clasters[2] == cl3 and clasters[3] == cl4 and clasters[4] == cl5:
        status = 'done'
    for cl in clasters:
        print(len(cl))
    return(clasters[0], clasters[1], clasters[2], clasters[3], clasters[4], status)


def move_centroid(c, cl):
    sr, sg, sb = 0, 0, 0
    for (r, g, b) in cl:
        sr += r
        sg += g
        sb += b
    n = len(cl)
    c = (sr//n, sg//n, sb//n)
    return(c)
        
    
def create_rectangles(c, imheight, imwidth, centroids):
    a = imheight//5
    for i in range(4):
        c.create_rectangle(0,1+i*a,imwidth//5, (i+1)*a, outline = 'white', fill = get_color(centroids[4-i]))
    c.create_rectangle(0,1+4*a,imwidth//5,5*a+(imheight-5*a), outline = 'white',fill = get_color(centroids[0]))  


root = Tk()
fr0 = Frame(root)
fr0.pack()
fr3 = Frame(root)
fr3.pack()
fr1 = Frame(fr0)
fr1.pack(side = LEFT)
fr2 = Frame(fr0)
fr2.pack(side = LEFT)
pilImage = Image.open("my_image.jpg")
image = ImageTk.PhotoImage(pilImage)
im = Image.open('my_image.jpg')
(imwidth, imheight) = im.size
label = tk.Label(fr1, image = image)
label.pack()
c = Canvas(fr2, width = imwidth//5+2, height = imheight)
c.pack()
cl1, cl2, cl3, cl4, cl5 = [], [], [], [], []
status = 'progress'
c1, c2, c3, c4, c5 = init_centroid(im, imheight, imwidth)
i = 0
while status == 'progress':
    cl1, cl2, cl3, cl4, cl5, status = get_clasters(im, c1, c2, c3, c4, c5, cl1, cl2, cl3, cl4, cl5, status)
    c1 = move_centroid(c1, cl1)
    c2 = move_centroid(c2, cl2)
    c3 = move_centroid(c3, cl3)
    c4 = move_centroid(c4, cl4)
    c5 = move_centroid(c5, cl5)
    print(' ')
cls = [(c1, len(cl1)), (c2, len(cl2)), (c3, len(cl3)), (c4, len(cl4)), (c5, len(cl5))]
cls.sort(key = lambda param: param[1])
centroids = [x[0] for x in cls]
create_rectangles(c, imheight, imwidth, centroids)

root.mainloop()
