from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3' #/// : 현재 디렉토리 - //// : 절대 디렉토리
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 각종 warning들 무시하기


db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)


@app.route('/')
def index():
    item_list = Item.query.all()

    return render_template('index.html', item_list=item_list)

@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form.get('name')
    price = int(request.form.get('price'))
    print(Item.query.filter_by(name=name))
    if Item.query.filter_by(name=name):
        redirect(url_for('index'))
    else:
        new_item = Item(name=name, price=price)

        db.session.add(new_item)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    item = Item.query.get(item_id)


    db.session.delete(item)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)