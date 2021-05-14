from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import db

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db.init_app(app)

def main():
    db.create_all()
    
if __name__ == '__main__':
    with app.app_context():
        main()




