from tkinter import *
from PIL import Image, ImageTk
from ch_file import choose_file, get_filename
from DC import getDC, to16

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
        self.state_label = Label(self.fr4, text = "Example")
        self.state_label.pack()
        self.im = Image.open("start.png")
        image = ImageTk.PhotoImage(self.im)
        (self.imwidth, self.imheight) = self.im.size
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
        k = 5
        a = self.imheight//k
        for i in range(k-1):
            self.c.create_rectangle(0,1 + i*a, self.imwidth//5, (i+1)*a, outline = 'white', fill = get_color(centroids[4-i]))
        self.c.create_rectangle(0,1 + 4*a, self.imwidth//5, 5*a + (self.imheight-5*a), outline = 'white', fill = get_color(centroids[0]))
        
    def get_result(self):
        self.im = Image.open(get_filename(choose_file()))
        self.state_label.configure(text = "Processing")
        self.root.update()
        new_image = ImageTk.PhotoImage(self.im)
        (self.imwidth, self.imheight) = self.im.size
        self.image_label.configure(image = new_image)
        self.image_label.image = new_image
        self.c.destroy()
        self.c = Canvas(self.fr3, width = self.imwidth//5+2, height = self.imheight)
        self.c.pack()
        clasters = getDC(self.im, self.imheight, self.imwidth)
        self.state_label.configure(text = "Done")
        self.create_rectangles(clasters)
        self.root.update()
        
w = Window()
