from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from myblog import db
from myblog.models import Post
from myblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/new_post', methods=['GET', 'POST'])
def create():
    create_form = PostForm()
    if create_form.validate_on_submit():
        new_post = Post(title=create_form.title.data,
                        content=create_form.content.data,
                        author=current_user)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('create.html', title='Create Post', form=create_form, legend='New Post')

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        post_form.title.data = post.title
        post_form.content.data = post.content
    return render_template('create.html', title='Update Post', form=post_form, legend='Update Post')

@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))