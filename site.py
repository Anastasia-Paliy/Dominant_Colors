from flask import Flask, render_template

site = Flask(__name__)


@site.route('/')  # отслеживаем главную стр
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

if __name__ == "__main__":
    site.run(debug=False)