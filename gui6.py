from tkinter import *
from PIL import Image, ImageTk
from ch_file import choose_file, get_filename
from newDC6 import getDC, to16

def get_color(c):
    color = '#'+to16(c[0])+to16(c[1])+to16(c[2])
    return(color)

class Window:
    def __init__(self):
        self.root = Tk()      
        self.root.title("Dominant Colors")
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
        self.button = Button(self.fr1, text = "Choose image", command = lambda: self.get_result())
        self.button.pack()
        self.state_label = Label(self.fr4, text = "Upload your image")
        self.state_label.pack()
        self.img = Image.open("start.png")
        image = ImageTk.PhotoImage(self.img)
        (self.imwidth, self.imheight) = self.img.size
        self.image_label = Label(self.fr2, image = image)
        self.image_label.pack()
        self.root.resizable(0,0)
        self.fr3 = Frame(self.fr23)
        self.fr3.pack(side = LEFT)
        self.c = Canvas(self.fr3, width = 0, height = 0)
        
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
        
        
    def get_result(self):
        file = get_filename(choose_file())
        print(file)
        self.img = Image.open(file)
        self.state_label.configure(text = "Processing")
        self.root.update()
        new_image = ImageTk.PhotoImage(self.img)
        (self.imgwidth, self.imgheight) = self.img.size
        (self.imwidth, self.imheight) = (self.imgwidth//10, self.imgheight//10)
        self.im = self.img
        self.im.thumbnail((self.imwidth, self.imheight))
        self.image_label.configure(image = new_image)
        self.image_label.image = new_image
        clasters, self.k = getDC(self.im, self.imheight, self.imwidth)
        self.c.destroy()
        self.c = Canvas(self.fr3, width = self.imgwidth//self.k+2, height = self.imgheight)
        self.c.pack()
        self.state_label.configure(text = "Done")
        self.create_rectangles(clasters)
        self.root.update()
        
w = Window()
