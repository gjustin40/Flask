import os
import secrets

from PIL import Image

from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required


from myblog import app, db, login_manager, bcrypt
from myblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from myblog.models import User, Post


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    print('aaaaaaaaaa', page)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(reg_form.password.data).decode('utf-8')
        user = User(username=reg_form.username.data,
                    password=hashed_password,
                    email=reg_form.email.data,)
        db.session.add(user)
        db.session.commit()        
        flash(f'Account created for {reg_form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=reg_form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check Email and Password', 'danger')
    return render_template('login.html', title='Login', form=login_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
    
# from pathlib import Path
def save_picture(form_picture):
    fname_hex = secrets.token_hex(8)
    _, ext_name = os.path.splitext(form_picture.filename)
    picture_fname = fname_hex + ext_name
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fname)
    
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    
    return picture_fname

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    update_form = UpdateAccountForm()
    if update_form.validate_on_submit():
        if update_form.picture.data:
            picture_fname = save_picture(update_form.picture.data)
            current_user.image_file = picture_fname
        current_user.username = update_form.username.data
        current_user.email = update_form.email.data
        db.session.commit()
        flash('Your Account have been Updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email
        
    img_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', img_file=img_file, form=update_form)

@app.route('/new_post', methods=['GET', 'POST'])
def create():
    create_form = PostForm()
    if create_form.validate_on_submit():
        new_post = Post(title=create_form.title.data,
                        content=create_form.content.data,
                        author=current_user)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create.html', title='Create Post', form=create_form, legend='New Post')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
        
    post_form = PostForm()
    if post_form.validate_on_submit():
        post.title = post_form.title.data
        post.content = post_form.content.data
        db.session.commit()
        flash('Your post have been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        post_form.title.data = post.title
        post_form.content.data = post.content
    return render_template('create.html', title='Update Post', form=post_form, legend='Update Post')

@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)