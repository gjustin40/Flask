from datetime import datetime

from flask import Blueprint, render_template, url_for, redirect, request, g

from app import db
from app.models import Question, Answer
from app.forms import AnswerForm
from app.views.auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<int:question_id>', methods=['POST', 'GET'])
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            content = request.form['content']
            answer = Answer(content=content, create_date=datetime.now(), user=g.user)
            question.answer_set.append(answer)
            db.session.commit()

            return redirect(url_for('question.detail', question_id=question_id))
    
    return render_template('question/question_detail.html', question=question, form=form)