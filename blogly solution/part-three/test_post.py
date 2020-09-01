from unittest import TestCase

from app import app
from models import db, Post, User
from .seed import seed_db



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True


class PostTestCase(TestCase):


    def setUp(self):
        seed_db()


    def tearDown(self):
        # This seems to be necessary to keep later tests from hanging
        # (Maybe I can't drop_all() if a transaction is in progress?)
        db.session.rollback()


    # -----------------------------------------------------


    def test_relation(self):
        post = Post.query.get(1)
        self.assertEqual(post.user.first_name, 'Sam')


    def test_new(self):
        user = User.query.get(1)
        post = Post(title='Three', content='Three', user_id=user.id)
        db.session.add(post)
        db.session.commit()
        self.assertEqual(Post.query.count(), 4)


    def test_edit(self):
        post = Post.query.get(1)
        post.title = 'foobar Post 1'
        db.session.commit()
        posts = Post.query.filter_by(title='foobar Post 1').all()
        self.assertEqual(len(posts), 1)
    

    def test_delete(self):
        self.assertEqual(Post.query.count(), 3)
        db.session.delete( Post.query.get(2) )
        self.assertEqual(Post.query.count(), 2)


    def test_delete_cascade(self):
        self.assertEqual(Post.query.count(), 3)
        user = User.query.get(1)
        db.session.delete(user)
        self.assertEqual(Post.query.count(), 1)