from flask import Blueprint, url_for, render_template, flash, request, redirect
from werkzeug.security import generate_password_hash

from app import db
from app.forms import UserCreateForm
from app.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        passowrd=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하고 있는 사용자입니다.')
    return render_template('auth/signup.html', form=form)