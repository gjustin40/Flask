from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vote.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(50), nullable=False)
    choices = db.relationship('Choice', backref='question')

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice_text = db.Column(db.String(50), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    
    def __init__(self, id=id, choice_text=choice_text, question_id=question_id):
        self.id = id
        self.choice_text = choice_text
        self.question_id = question_id

    def __repr__(self):
        return f'{self.question_id} --- {self.choice_text}'

@app.route('/')
@app.route('/index')
def index():

    question_list = Question.query.all()

    return render_template('index.html', question_list=question_list)

@app.route('/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':
        new_question = request.form.get('question')
        new_choice1 = request.form.get('choice1')
        new_choice2 = request.form.get('choice2')
        new_choice3 = request.form.get('choice3')

        question = Question(question_text=new_question)
        choice1 = Choice(choice_text=new_choice1, question=question)
        choice2 = Choice(choice_text=new_choice2, question=question)
        choice3 = Choice(choice_text=new_choice3, question=question)

        db.session.add(question)
        db.session.add_all([choice1, choice2, choice3])
        db.session.commit()

        return redirect(url_for('index'))

    else:
        return render_template('add.html')

@app.route('/detail/<int:id>')
def detail(id):

    question = Question.query.get(id)
    choice_list = question.choices
    print('----------------------------')
    print(choice_list)

    return render_template('detail.html', choice_list=choice_list)

if __name__ == '__main__':
    app.run(debug=True)

