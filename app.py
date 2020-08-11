"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False

connect_db(app)
db.create_all()


@app.route('/')
def list_users():
    """redirect to list of users"""
  
    return redirect('/users')

@app.route('/users')
def user_index():
    """show all users with links"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new')
def show_form():
    """show a form to add a user"""
    return render_template('/users/form.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """post form to add a new user then go back to users page"""
    first_name = request.form['fname']
    last_name = request.form['lname']
    image_url = request.form['img']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url or None)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details info of a given user"""
    user = User.query.get_or_404(user_id)
    return render_template('/users/details.html',user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """show a form to edit user info"""
    user = User.query.get_or_404(user_id)
    return render_template('/users/edit.html, user=user')

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """edit a user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['fname']
    user.last_name = request.form['lname']
    user.image_url = request.form['img']

    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """delete a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

