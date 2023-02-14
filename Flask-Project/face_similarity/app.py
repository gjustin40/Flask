from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import cv2
import numpy as np
# from crawling import get_info
from model import get_rank

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/distance', methods=['POST'])
def distance():
    
    if request.method == 'POST':
        image = request.files.get('image')
        image_path = 'static/img/user_input/' + image.filename
        image.save(image_path)



        me_cropped, result, top_distance = get_rank(image_path)
        name_list = [name for name, _ in result]
        cropped_top = [f'{name}.jpg' for name in name_list]
        print(cropped_top)
                
        return render_template('result.html',
                               me_cropped=me_cropped,
                               result=result,
                               top_distance=top_distance,
                               cropped_top=cropped_top,
                               image_path=image_path)
        
    return 'classification page'

if __name__ == '__main__':
    app.run(debug=True)