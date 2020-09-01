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

        user = User(first_name="John", last_name="Doe", image_url="https://www.google.com/imgres?imgurl=https%3A%2F%2Fsrkheadshotday.com%2Fwp-content%2Fuploads%2FKen_Nguyen_Headshot_16H3626.jpg&imgrefurl=https%3A%2F%2Fsrkheadshotday.com%2Fblog%2Fthe-best-tie-knot-for-your-headshot%2F&tbnid=f0mePlVDhAIxNM&vet=12ahUKEwihs4-86o_rAhVV454KHSFmCCIQMygOegUIARDuAQ..i&docid=UobcMAJU5BRp9M&w=1710&h=1140&q=head%20shot&ved=2ahUKEwihs4-86o_rAhVV454KHSFmCCIQMygOegUIARDuAQ")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        post = Post(title="teacher", content="abc", user_id="1")
        db.session.add(post)
        db.session.commit()

        self.post = post
        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
    
    def test_homepage(self):
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            html = response.get_data(as_text=True)
            self.AssertIn("<h1>Blogly Recent Posts</h1>", html)

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Doe, John', html)

    def test_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('src="https://www.google.com/imgres?imgurl=https%3A%2F%2Fsrkheadshotday.com%2Fwp-content%2Fuploads%2FKen_Nguyen_Headshot_16H3626.jpg&imgrefurl=https%3A%2F%2Fsrkheadshotday.com%2Fblog%2Fthe-best-tie-knot-for-your-headshot%2F&tbnid=f0mePlVDhAIxNM&vet=12ahUKEwihs4-86o_rAhVV454KHSFmCCIQMygOegUIARDuAQ..i&docid=UobcMAJU5BRp9M&w=1710&h=1140&q=head%20shot&ved=2ahUKEwihs4-86o_rAhVV454KHSFmCCIQMygOegUIARDuAQ"', html)
           
    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "James", "last_name": "Smith"}
            response = client.post("/users/new", data=d, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>James Smith</h1>", html)
    def test_edit_user(self):
        with app.test_client() as client:
            d = {first_name: Jane, last_name: Doe}
            response = client.post(f'/users/{self.user_id}/edit', data = d,follow_redirects=True) 
            html = response.get_data(as_text=True)
            
            user = User.query.get(self.user_id)
            self.assertEqual("Jane", html)
            
    
    def test_delete_user(self):
        with app.test_client() as client:
    
            response = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Allen,Dave",html)

            response = client.get(f"/users/{self.user_id}/delete", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            response = client.get('/users')
            html = response.get_data(as_text=True)
            self.assertNotIn('Allen,Dave', html)

#------------------------------------

    def test_list_posts(self):
        with app.test_client() as client:
            response = client.get("/posts")
            html = resp.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Blogly Recent Posts</h1>', html)
           
    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "queen", "content": "wyz"}
            resp = client.post(f"/users/1/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>queen</h1>", html)
            self.assertIn("<p>wyz</p>", html)

#------------------------------------
def test_tag_list(self):
    with app.test_client() as client:
            response = client.get("/tags")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Blogly Recent Posts</h1>', html)

def test_tag_new(self):
     with app.test_client() as client:
        d = {"name": "fun"}
        response = client.post(f"/tags/new", data=d, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("fun", html)
        