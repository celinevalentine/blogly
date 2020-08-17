from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


DEFAULT_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Circle-icons-profile.svg/1024px-Circle-icons-profile.svg.png"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

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

    def __repr__(self):
        return f"<User {self.first_name}>"

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
    created_at=db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='post')

    def __repr__(self):
        return f"<Post {self.content} {self.uesr_id} {self.first_name} >"
    

    


    