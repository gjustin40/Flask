from flask import Blueprint, url_for, redirect
from app.models import Question

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_flask():
    return 'Hello, Flask!'

@bp.route('/')
def index():
    return redirect(url_for('question._list'))
