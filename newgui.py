from tkinter import *
from PIL import Image, ImageTk, ImageGrab, EpsImagePlugin, ImageDraw
from DC import getDC, to16
import io
import os
import subprocess
#import win32gui


def get_color(c):
    color = '#'+to16(c[0])+to16(c[1])+to16(c[2])
    return(color)

class Window:
    def __init__(self, image):
        self.root = Tk()
        self.root.resizable(0,0)
        
        self.fr0 = Frame(self.root)
        self.fr0.pack()
        self.fr1 = Frame(self.fr0)
        self.fr1.pack()
        self.fr23 = Frame(self.fr0)
        self.fr23.pack()
        self.fr4 = Frame(self.fr0)
        self.fr4.pack()
        self.fr2 = Frame(self.fr23)
        self.fr2.pack(side = LEFT)
        self.fr3 = Frame(self.fr23)
        self.fr3.pack(side = LEFT)
        
        self.img = Image.open(image)
        self.photo = Image.open(image)
        self.photo_image = ImageTk.PhotoImage(self.img)
        (self.imgwidth, self.imgheight) = self.img.size
        (self.imwidth, self.imheight) = (self.imgwidth//2, self.imgheight//2)
        self.im = self.img
        self.im.thumbnail((self.imwidth, self.imheight))
        self.image_label = Label(self.fr2, image = self.photo_image)
        self.image_label.pack()
        
        self.k = 5
        self.c = Canvas(self.fr3, width = self.imgwidth//self.k+2, height = self.imgheight)
        self.c.pack()
        clasters = getDC(self.im, self.imheight, self.imwidth)
        self.create_rectangles(clasters)
        self.root.update()
        
        #self.getter(self.c)

        self.save_as_png("my_saved_image")
        
        #self.c.postscript(file = "file_name.ps", colormode = 'color')
        
        #self.get_it() working!

        #self.get_result()

        self.draw_rectangles(clasters)
        self.get_image()
        
        self.root.mainloop()


    def create_rectangles(self, clasters):
        centroids = [x[0] for x in clasters]
        points = [x[1] for x in clasters]
        print(centroids)
        print(points)
        total = sum(points)
        frequencies = [point/total for point in points]
        print(frequencies)
        a = self.imgheight
        b = self.imgwidth//self.k
        y = [0]
        s = 0
        for i in range(self.k):
            s = round(s + frequencies[i], 3)
            y.append(s)
        print(y)
        for i in range(self.k-1):
            self.c.create_rectangle(0,1 + a*y[i], b, a*y[i+1], outline = 'white', fill = get_color(centroids[i]))
        self.c.create_rectangle(0,1 + a*y[self.k-1], b, a, outline = 'white', fill = get_color(centroids[self.k-1]))
        for i in range(self.k):
            print(get_color(centroids[i]))


    def save_as_png(self, filename):
        EpsImagePlugin.gs_windows_binary =  r'C:\Program Files\gs\gs9.54.0\bin\gswin64c'
        self.c.postscript(file = filename + '.eps') 
        img = Image.open(filename + '.eps') 
        img.save(filename + '.png', 'png')
        self.rectangles = img


    def get_result(self):
        print((self.imgwidth, self.imgheight))
        (w, h) = self.rectangles.size
        print((w,h))
        (w1, h1) = round(w*self.imgheight/h), self.imgheight
        print((w1, h1))
        self.rectangles.thumbnail((w1,h1), Image.ANTIALIAS)
        print(self.rectangles.size)
        image1_size = (self.imgwidth, self.imgheight)
        image2_size = (w1, h1)
        print(image1_size,image2_size)
        newImage = Image.new('RGB',(image1_size[0]+image2_size[0], image1_size[1]), (250,250,250))
        newImage.paste(self.photo,(0,0))
        newImage.paste(self.rectangles,(image1_size[0],0))
        print(newImage.size)
        #newImage.show()
        newImage.save('result.png','png')
        

    def draw_rectangles(self, clasters):
        a = self.imgheight
        b = self.imgwidth//self.k
        
        rects = Image.new('RGB', (b, a), (255, 255, 255))
        draw = ImageDraw.Draw(rects)
        
        centroids = [x[0] for x in clasters]
        points = [x[1] for x in clasters]
        print(centroids)
        print(points)
        total = sum(points)
        frequencies = [point/total for point in points]
        print(frequencies)
        y = [0]
        s = 0
        for i in range(self.k):
            s = round(s + frequencies[i], 3)
            y.append(s)
        print(y)
        
        for i in range(self.k-1):
            draw.rectangle((0, a*y[i], b-1, a*y[i+1]), fill = get_color(centroids[i]), outline = (255, 255, 255))
        draw.rectangle((0, a*y[self.k-1], b-1, a-1), fill = get_color(centroids[self.k-1]), outline = (255, 255, 255))
        rects.save("pallete.png", "png")
        

    def get_image(self):
        rects = Image.open("pallete.png")
        image1_size = (self.imgwidth, self.imgheight)
        image2_size = rects.size
        print(image1_size, image2_size)
        newImage = Image.new('RGB',(image1_size[0]+image2_size[0], image1_size[1]), (250,250,250))
        newImage.paste(self.photo,(0,0))
        newImage.paste(rects,(image1_size[0],0))
        print(newImage.size)
        newImage.show()
        newImage.save('result.png','png')

        
        
    """        
    def get_it(self):
        EpsImagePlugin.gs_windows_binary =  r'C:\Program Files\gs\gs9.54.0\bin\gswin64c'
        ps = self.c.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        img.save('filename.jpg', 'jpeg')
            
    def getter(self, widget):
        x = self.root.winfo_rootx() + widget.winfo_x()
        y = self.root.winfo_rooty() + widget.winfo_y()
        x1 = x + widget.winfo_width()
        y1 = y + widget.winfo_height()
        print((x,y,x1,y1))
        ImageGrab.grab().crop((x, y, x1, y1)).save("my_img.png")    

    def get_image(self):
        HWND = self.c.winfo_id()  # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND)  # get the coordinate of the canvas
        im = ImageGrab.grab(rect).save("my_wanted_img.png")
    """        
 
w = Window("im1.jpg")
