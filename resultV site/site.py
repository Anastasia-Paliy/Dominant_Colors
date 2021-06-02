from flask import Flask, render_template, request
from DC import Window

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


@site.route('/starting', methods=['GET'])
def starting():
    return render_template('starting.html')


@site.route('/result', methods=['POST'])
def result():
    img = request.files['uploadfile']
    filename = img.filename.rsplit('.', 1)
    try:
        if allowed_file(filename):
            Window(img, site.root_path, filename[0])
            return render_template('result.html', filename=filename[0])
        else:
            return render_template('error.html')
    except IndexError:
        return render_template('starting.html')


if __name__ == "__main__":
    site.run()
