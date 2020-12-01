from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


#################### Model ################################################################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

food_log = db.Table('food_log',
    db.Column('food_id', db.Integer, db.ForeignKey('food.food_id')),
    db.Column('log_id', db.Integer, db.ForeignKey('log.log_id'))
)

class Food(db.Model):
    food_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    proteins = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)

    logs = db.relationship('Log', secondary=food_log, backref='foods', lazy='dynamic')

    @property
    def calories(self):
        return self.proteins*4 + self.carbs*4 + self.fats*4

class Log(db.Model):
    log_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)

    @property
    def sum_proteins(self):
        return self.date.foods


###########################################################################################################

######################################## Route ############################################################
@app.route('/')
def index():
    log_list = Log.query.order_by(Log.date.desc()).all()

    log_and_food_list = []
    
    
    for log in log_list:
        proteins, carbs, fats, calories = 0, 0, 0, 0
        food_sum_dict = {}
        for food in log.foods:
            proteins += food.proteins
            carbs += food.carbs
            fats += food.fats
            calories += food.calories
        
        food_sum_dict['log_date'] = log
        food_sum_dict['proteins'] = proteins
        food_sum_dict['carbs'] = carbs
        food_sum_dict['fats'] = fats
        food_sum_dict['calories'] = calories

        log_and_food_list.append(food_sum_dict)

    return render_template('index.html', log_list=log_list, log_and_food_list=log_and_food_list)

@app.route('/add')
def add():
    food_list = Food.query.all()

    return render_template('add.html', food_list=food_list, edit_food=None)

@app.route('/add_item', methods=['POST'])
def add_item():

    if request.method == 'POST':

        name = request.form.get('food-name')
        proteins = request.form.get('proteins')
        carbs = request.form.get('carbs')
        fats = request.form.get('fats')

        edit_food_id = request.form.get('edit-item')
        if edit_food_id:
            edit_food = Food.query.get(edit_food_id)
            edit_food.name = name
            edit_food.proteins = proteins
            edit_food.carbs = carbs
            edit_food.fats = fats


        else:
            new_food = Food(
                name=name,
                proteins=proteins,
                carbs=carbs,
                fats=fats
            )

            db.session.add(new_food)

        db.session.commit()

    return redirect(url_for('add'))

@app.route('/edit_item/<int:food_id>')
def edit_item(food_id):
    food_list = Food.query.all()
    edit_food = Food.query.get(food_id)

    return render_template('add.html', food_list=food_list, edit_food=edit_food)

@app.route('/delete_item/<int:food_id>')
def delete_item(food_id):
    delete_food = Food.query.get(food_id)
    db.session.delete(delete_food)
    db.session.commit()

    return redirect(url_for('add'))

@app.route('/view/<int:log_id>')
def view(log_id):
    food_list = Food.query.all()
    selected_log = Log.query.get(log_id)

    proteins_sum, carbs_sum, fats_sum, calories_sum = 0, 0, 0, 0
    for food in selected_log.foods:
        proteins_sum += food.proteins
        carbs_sum += food.carbs
        fats_sum += food.fats
        calories_sum += food.calories

    sum_dict = {
        'proteins_sum': proteins_sum,
        'carbs_sum': carbs_sum,
        'fats_sum': fats_sum,
        'calories_sum': calories_sum
        }

    return render_template('view.html', food_list=food_list, selected_log=selected_log, sum_dict=sum_dict)

@app.route('/add_date', methods=['POST'])
def add_date():
    if request.method == 'POST':
        get_date = request.form.get('date')
        get_date = datetime.strptime(get_date, '%Y-%m-%d')
        new_date = Log(date=get_date)

        db.session.add(new_date)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/add_log_food/<int:log_id>', methods=['POST'])
def add_log_food(log_id):
    selected_log = Log.query.get(log_id)

    if request.method == 'POST':
        food_id = request.form.get('food-select')
        selected_food = Food.query.get(food_id)
        selected_log.foods.append(selected_food)

        db.session.commit()

    return redirect(url_for('view', log_id=log_id))

@app.route('/delete_log_food/<int:log_id>/<int:food_id>')
def delete_log_food(log_id, food_id):
    my_log = Log.query.get(log_id)
    my_food = Food.query.get(food_id)
    my_log.foods.remove(my_food)

    db.session.commit()

    return redirect(url_for('view', log_id=log_id))


############################################################################################################
if __name__ == '__main__':
    app.run(debug=True)
