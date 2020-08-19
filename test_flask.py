from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        user = User(first_name="John_t", last_name="Doe_t")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        Post.query.delete()

        post = Post(title="teacher_t", content="abc_t", user_id="1")
        db.session.add(post)
        db.session.commit()

        self.post = post
        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John_t', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>John_t Doe_t</h1>', html)
           
    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "James_t", "last_name": "Smith_t"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>James_t Smith_t</h1>", html)

    def test_show_user_form(self):
       with app.test_client() as client:
            resp = client.get(f"/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<label>First Name</label>', html)

    def test_list_posts(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Blogly Recent Posts</h1>', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>teacher_t</h1>', html)
           
    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "king_t", "content": "wyz_t"}
            resp = client.post("/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>king_t</h1>", html)
            self.assertIn("<p>wyz_t</p>", html)

    def test_show_post_form(self):
       with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button>Add</button>', html)
