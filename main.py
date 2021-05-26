from tkinter import Tk, Frame, Button, Label, Image, Canvas, LEFT

from PIL import ImageTk
from flask import Flask, render_template, request, make_response

site = Flask(__name__)


@site.route('/')
def home():
    return render_template('home.html')


@site.route('/about')
def about():
    return render_template('about.html')


@site.route('/contacts')
def contacts():
    return render_template('contacts.html')


@site.route('/support')
def support():
    return render_template('support.html')


@site.route('/starting', methods=['POST', 'GET'])
def starting():
    if request.method == 'POST':
        image = request.form['uploadfile']
    else:
        return render_template('starting.html')


@site.route('/result')
def result():
    return render_template('result.html')


@site.route('/')
def http_404_handler():
    return make_response("<h2>404 Error</h2>", 400)


if __name__ == "__main__":
    site.run(debug=True)
