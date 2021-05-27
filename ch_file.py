import tkinter
from tkinter import filedialog as fd
import os

directory = os.getcwd()+ '\\test_images'
x = len('\\test_images')


def choose_file():
    root = tkinter.Tk()
    root.withdraw()
    file_name = fd.askopenfilename(title = 'Choose file', initialdir = directory)
    if file_name:
        return file_name
    return None


def get_filename(file):
    path = os.path.dirname(file)
    l = len(path)
    filename = file[l+1-x: ]
    return filename