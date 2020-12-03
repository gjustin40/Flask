from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(50), nullable=False)
    user_phone = db.Column(db.Integer, nullable=True)


@app.route('/')
def go_to_index():

    return redirect(url_for('index'))

@app.route('/index')
def index():

    user_list = User.query.all()

    return render_template('index.html', user_list=user_list)

@app.route('/add_user', methods=['POST'])
def add_user():

    if request.method == 'POST':
        user_name = request.form.get('name')
        user_email = request.form.get('email')
        user_phone = request.form.get('phone')

        new_user = User(
            user_name=user_name,
            user_email=user_email,
            user_phone=user_phone
        )

        db.session.add(new_user)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/update_user', methods=['POST'])
def update_user():

    if request.method == 'POST':
        user_id = request.form.get('id')
        user = User.query.get(user_id)
        
        user.user_name = request.form.get('name')
        user.user_email = request.form.get('email')
        user.user_phone = request.form.get('phone')

        db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
