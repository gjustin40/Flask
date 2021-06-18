from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
posts = [
    {'title': 'Post1',
     'author': 'author1',
     'date_posted': '2000-1-1',
     'content': 'content1'},
     
    {'title': 'Post2',
     'author': 'author2',
     'date_posted': '2000-1-2',
     'content': 'content2'},
]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(100), unique=True, default='image.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.datetime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='home', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='about')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', title='registration')

if __name__ == '__main__':
    app.run(debug=True)