from flask import Flask, render_template, redirect
from wtforms_fields import *

app = Flask(__name__)
app.secret_key = 'aaa'

@app.route('/', methods=['POST', 'GET'])
def index():

    form = RegForm()
    form.validate_on_submit()

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)