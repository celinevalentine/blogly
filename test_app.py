from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEGUB_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['TESTING'] = True

db.drop_all()
db.create_all()


class AppTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""
        User.query.delete()
        Post.query.delete()
        Tag.query.delete()

        user = User(first_name="John", last_name="Doe", image_url="www.image.com")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        post = Post(title="teacher", content="abc", user_id="1")
        db.session.add(post)
        db.session.commit()

        self.post = post
        self.post_id = post.id

        tag = Tag(name="fun")
        db.session.add(tag)
        db.session.commit()

        self.tag = tag
        self.tag_id = tag.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
    
    def xtest_homepage(self):
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            html = response.get_data(as_text=True)
            self.assertIn("<h1>Blogly Recent Posts</h1>", html)

    def xtest_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)

    def xtest_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('src="www.image.com"', html)
           
    def xtest_add_user(self):
        with app.test_client() as client:
            d = {"fname": "James", "lname": "Smith", "img": "None"}
            response = client.post("/users/new", data=d, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("James Smith", html)
    def xtest_edit_user(self):
        with app.test_client() as client:
            d = {"fname": "Jane", "lname": "Doe", "img": "123.com"}
            response = client.post(f'/users/{self.user_id}/edit', data = d,follow_redirects=True) 
            html = response.get_data(as_text=True)
            
            user = User.query.get(self.user_id)
            self.assertIn("Jane Doe", html)
            
    
    def xtest_delete_user(self):
        with app.test_client() as client:
    
            d = {"fname": "Jane", "lname": "Doe", "img": "123.com"}
            response = client.post(f'/users/{self.user_id}/delete', data = d,follow_redirects=True) 
            html = response.get_data(as_text=True)
            
            user = User.query.get(self.user_id)
            self.assertNotIn("Jane Doe", html)

#------------------------------------

    def xtest_list_posts(self):
        with app.test_client() as client:
            response = client.get("/")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Blogly Recent Posts', html)


    def xtest_add_post(self):
        with app.test_client() as client:
            d = {"title": "queen", "content": "wyz"}
            response = client.post(f"/users/1/posts/new", data=d, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("queen", html)
    

#------------------------------------
def xtest_tag_list(self):
    with app.test_client() as client:
            response = client.get("/tags")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Blogly Recent Posts', html)

def test_tag_new(self):
     with app.test_client() as client:
        d = {"name": "fun"}
        response = client.post(f"/tags/new", data=d, follow_redirects=True)
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("fun", html)
        