from flask import Flask
from models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pablsvabiuayfz:20870cf897d1fcc424dea780b813afcc1ff5af35190470652cd81044d4e099c1@ec2-52-4-111-46.compute-1.amazonaws.com:5432/d62s5lvrndg678'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db.init_app(app)

def main():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        main()