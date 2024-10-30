from flask import render_template
from views.TD1Views.hello import hello_tp1
from views.TD1Views import image_py


def index():
    return render_template('indexTD1.html')

def hello():
    return hello_tp1()

def image():
    return image_py.image_page()

# @tp1.route('/uploads/<filename>')
def uploaded_file(filename):
    return image_py.uploaded_file(filename)

