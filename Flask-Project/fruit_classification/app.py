from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import cv2
import numpy as np
from crawling import get_info
from model import fruit_classification
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classification', methods=['POST'])
def classification():

    if request.method == 'POST':
        image = request.files.get('image')
        image_path = 'static/img/user_input/' + image.filename
        image.save(image_path)

        fruit_name = fruit_classification(image_path)
        fruit_path = image_path
        fruit = {
            'name': fruit_name,
            'path': fruit_path,
            'desc': get_info(fruit_name)
        }

        return render_template('result2.html', fruit=fruit, image_path=image_path)
    return 'classification page'

@app.route('/error')
def error():
    return ''

# @app.route('/result')
# def result():
#     return render_template('result.html', fruit=fruit)

if __name__ == '__main__':
    app.run(debug=True)
    