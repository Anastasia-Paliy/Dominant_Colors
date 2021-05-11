from tkinter import *
from tkinter import filedialog as fd
import string
import os


directory = os.getcwd()

def choose_file():
    file_name = fd.askopenfilename(title = 'Choose file', initialdir = directory)
    if file_name:
        return file_name
    return None

def get_filename(file):   
    path = os.path.dirname(file)
    l = len(path)
    filename = file[l+1: ]
    return filename

