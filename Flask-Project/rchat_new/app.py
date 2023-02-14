from flask import Flask, render_template, redirect, url_for, flash

from wtforms_fields import *
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from passlib.hash import pbkdf2_sha256

from models import *

app = Flask(__name__)
app.secret_key = 'later'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pablsvabiuayfz:20870cf897d1fcc424dea780b813afcc1ff5af35190470652cd81044d4e099c1@ec2-52-4-111-46.compute-1.amazonaws.com:5432/d62s5lvrndg678'
db = SQLAlchemy(app)

login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):

    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_password = pbkdf2_sha256.hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registered succesfully. Please login', 'success')

        return redirect(url_for('login'))

    return render_template('index.html', form=reg_form)


@app.route('/login', methods=['POST', 'GET'])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

        return 'Not Logged in'

    return render_template('login.html', form=login_form)


@app.route('/chat', methods=['GET', 'POST'])
def chat():

    if not current_user.is_authenticated:
        flash('Please login', 'danger')

        return redirect(url_for('login'))

    return 'Chat with me!'


@app.route('/logout', methods=['GET'])
def logout():

    logout_user()
    flash('You have logged out sucessfully', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
