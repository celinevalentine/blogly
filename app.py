"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def root():
    """show 5 most recent posts"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()  
    return render_template('posts/homepage.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """show 404 NOT found page"""
    return render_template('404.html'), 404

@app.route('/users')
def user_index():
    """show all users with links"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new')
def show_user_form():
    """show a form to add a user"""
    return render_template('users/add.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """post form to add a new user then go back to users page"""
    first_name = request.form['fname']
    last_name = request.form['lname']
    image_url = request.form['img']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url or None)
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} is added!")

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details info of a given user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/detail.html',user=user)

@app.route('/users/<int:user_id>/edit')
def user_edit_form(user_id):
    """show a form to edit user info"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """edit a user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['fname']
    user.last_name = request.form['lname']
    user.image_url = request.form['img']

    db.session.add(user)
    db.session.commit()
    flash(f"User{user.full_name} is edited!")
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """delete a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} is deleted!")
    return redirect('/users')

#Post route

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """show the post form to add a new post for a user"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/add.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """handle submission of the post form"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    new_post = Post(title=request.form['title'], content=request.form['content'],user_id=user_id, tags=tags)
    db.session.add(new_post)
    db.session.commit()
  
    flash(f"Post {new_post.title} of {user.full_name} is added!")
    return redirect (f"/users/{user.id}")

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """show posts from a user"""
    post = Post.query.get_or_404(post_id)
    
    return render_template('posts/detail.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """show edit post form"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """edit a post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    flash(f"Post {post.title} is edited!")

    return redirect (f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """delete a post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post {post.title} is deleted!")
    return redirect (f"/users/{post.user_id}")

# tag route
@app.route('/tags')
def list_tags():
    """list all tags"""
    tags = Tag.query.all()
    return render_template('tags/list.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    """show detail of a tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/detail.html', tag=tag)

@app.route('/tags/new')
def show_add_tag_form():
    """show add tag form"""
    
    posts = Post.query.all()
    return render_template('tags/add.html',posts=posts)

@app.route('/tags/new', methods=['POST'])
def add_tag():
    """handle add tag form"""
  
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    flash(f"Tag {new_tag.name} is added!")
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """show edit tag form"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag_form(tag_id):
    """ edit tag form"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
   
    db.session.add(tag)
    db.session.commit()
    flash(f"Tag {tag.name} is edited!")
    return redirect ("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """delete a post"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag {tag.name} is deleted!")
    return redirect ("/tags")



