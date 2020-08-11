from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

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
    image_url = db.Column(db.String(50), nullable=False, default= DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        """return full name"""
        return f"{self.first_name} {self.last_name}"

    