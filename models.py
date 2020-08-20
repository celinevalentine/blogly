import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"



"""Models for Blogly."""
class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                     nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default= DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        """return full name"""
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.Text,nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at=db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', backref=backref('posts', cascade="all, delete"))

    tags = db.relationship('Tag',secondary='post_tags',backref='posts')

    post_tags = db.relationship('PostTag', backref='posts')

    @property
    def format_date(self):
        """format time stamp"""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    
class Tag(db.Model):
    """blog tag"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    post_tags = db.relationship('PostTag',backref='tags')

class PostTag(db.Model):
    """mapping of a post to a tag"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"),primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"),primary_key=True)


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


    