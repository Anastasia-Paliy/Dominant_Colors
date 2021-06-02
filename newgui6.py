from PIL import Image, ImageDraw
from newDC6 import getDC, to16
from ch_file import choose_file, get_filename


def get_color(c):
    color = '#'+to16(c[0])+to16(c[1])+to16(c[2])
    return(color)


class Window:
    def __init__(self, image):
        self.img = Image.open(image)
        self.photo = Image.open(image)
        (self.imgwidth, self.imgheight) = self.img.size
        (self.imwidth, self.imheight) = (self.imgwidth//10, self.imgheight//10)
        self.im = self.img
        self.im.thumbnail((self.imwidth, self.imheight))

        clasters, self.k = getDC(self.im, self.imheight, self.imwidth)
        #self.k = min(5, self.k)
        self.draw_rectangles(clasters)
        self.get_image()
        

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
        newImage = Image.new('RGB',(image1_size[0]+image2_size[0], image1_size[1]), (250,250,250))
        newImage.paste(self.photo,(0,0))
        newImage.paste(rects,(image1_size[0],0))
        newImage.show()
        newImage.save('result.png','png')

     
 
w = Window(get_filename(choose_file()))
