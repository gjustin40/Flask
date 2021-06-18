from datetime import datetime

from flask import Blueprint, render_template, url_for, redirect, request

from app import db
from app.models import Question
from app.forms import QuestionForm

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc())

    return render_template('question/question_list.html', question_list=question_list)


@bp.route('detail/<int:question_id>')
def detail(question_id):
    question = Question.query.get_or_404(question_id)

    return render_template('question/question_detail.html', question=question)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = QuestionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print('validate 통과')
            question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
            db.session.add(question)
            db.session.commit()
            
            return redirect(url_for('main.index'))

    return render_template('question/question_form.html', form=form)