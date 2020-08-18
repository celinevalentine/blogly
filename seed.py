"""Seed file to make sample data for user db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
Dave_Allen = User(first_name='Dave', last_name="Allen", image_url='https://www.google.com/imgres?imgurl=https%3A%2F%2Fsrkheadshotday.com%2Fwp-content%2Fuploads%2FKen_Nguyen_Headshot_16H3626.jpg&imgrefurl=https%3A%2F%2Fsrkheadshotday.com%2Fblog%2Fthe-best-tie-knot-for-your-headshot%2F&tbnid=f0mePlVDhAIxNM&vet=12ahUKEwihs4-86o_rAhVV454KHSFmCCIQMygOegUIARDuAQ..i&docid=UobcMAJU5BRp9M&w=1710&h=1140&q=head%20shot&ved=2ahUKEwihs4-86o_rAhVV454KHSFmCCIQMygOegUIARDuAQ')
Dana_Pine = User(first_name='Dana', last_name="Pine", image_url='https://a57.foxnews.com/hp.foxnews.com/images/2020/08/320/180/5ab97ed145d3b286b7ff65f251387ede.jpg')
Mark_Thompson = User(first_name='Mark', last_name="Thompson", image_url='https://www.google.com/imgres?imgurl=https%3A%2F%2Fi.pinimg.com%2Foriginals%2Fe3%2F7e%2F0e%2Fe37e0e25686c2139b281a57a5b4906f2.jpg&imgrefurl=https%3A%2F%2Fwww.pinterest.com%2Fpin%2F460704236854562822%2F&tbnid=GBQUgulcaGKMqM&vet=12ahUKEwihs4-86o_rAhVV454KHSFmCCIQMygDegUIARDYAQ..i&docid=ggzHqVML9AbjqM&w=3744&h=5616&q=head%20shot&ved=2ahUKEwihs4-86o_rAhVV454KHSFmCCIQMygDegUIARDYAQ')

post1 = Post(title='teacher', content="abcdefg", created_at="2020.01.01", user_id=2)
post2 = Post(title='king', content="uxmn", created_at="2020.01.02", user_id=2)

tag1 = Tag(name="teacher")
tag2 = Tag(Name="king")

pt1 = PostTag(post_id=1, tag_id=1)
pt2 = PostTag(post_id=2, tag_id=2)


db.session.add(Dave_Allen)
db.session.add(Dana_Pine)

db.session.commit()

db.session.add(post1)
db.session.add(post2)

db.session.commit()

db.session.add(pt1)
db.session.add(pt2)

db.session.commit()

