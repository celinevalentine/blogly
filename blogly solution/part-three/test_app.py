import re
from unittest import TestCase

from app import app
from models import db, Post, User
from .seed import seed_db



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True


class AppTestCase(TestCase):


    def setUp(self):
        seed_db()


    def tearDown(self):
        # This seems to be necessary to keep later tests from hanging
        # (Maybe I can't drop_all() if a transaction is in progress?)
        db.session.rollback()

    
    # -----------------------------------------------------


    def test_home(self):
        with app.test_client() as client:
            response = client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Jim's Blogly</div>", html)


    def test_datetime_filter(self):
        with app.test_client() as client:
            response = client.get('/')
        self.assertEqual(response.status_code, 200)
        regex = r'By: Sam Houston | \d\d? \w\w\w 20\d\d @ \d\d:\d\d:\d\d'
        html = response.get_data(as_text=True)
        self.assertRegex(html, regex)


    # -----------------------------------------------------


    def test_user_list(self):
        with app.test_client() as client:
            response = client.get('/users')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Alda, Alan', html)


    def test_user_detail(self):
        with app.test_client() as client:
            response = client.get( f'/users/1' )
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('<h1>Sam Houston', html)
        self.assertIn('src="https://upload.wikimedia.org/wikipedia/commons/1/17/Samuel_houston.jpg"', html)


    def test_user_new(self):
        d = { 'first_name': 'Joe', 'last_name': 'Papa', 'image_url': 'http://foo.com/me.jpg' }
        with app.test_client() as client:
            response = client.post('/users/new', data=d, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Papa, Joe', html)


    def test_user_delete(self):
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)
            self.assertIn('Houston, Sam', html)
            response = client.post( f'/users/1/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            response = client.get('/users')
            html = response.get_data(as_text=True)
            self.assertNotIn('Houston, Sam', html)


    # -----------------------------------------------------


    def test_post_list(self):
        with app.test_client() as client:
            response = client.get('/posts')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Post 1', html)


    def test_post_new(self):
        d = { 'title': 'Title 20', 'content': 'Content 20' }
        with app.test_client() as client:
            response = client.post(f'/users/1/posts/new', data=d, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)  # user detail page
        self.assertIn('Sam Houston', html)
        self.assertIn('Title 20', html)


    # -----------------------------------------------------


    def test_tag_list(self):
        with app.test_client() as client:
            response = client.get('/tags')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Seattle', html)


    def test_tag_new(self):
        d = { 'name': 'lasagne' }
        with app.test_client() as client:
            response = client.post(f'/tags/new', data=d, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)  # user detail page
        self.assertIn('<h1>lasagne</h1>', html)