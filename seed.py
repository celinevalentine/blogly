"""Seed file to make sample data for user db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
Dave_Allen = User(first_name='Dave', last_name="Allen", image_url='https://www.google.com/imgres?imgurl=https%3A%2F%2Fsrkheadshotday.com%2Fwp-content%2Fuploads%2FKen_Nguyen_Headshot_16H3626.jpg&imgrefurl=https%3A%2F%2Fsrkheadshotday.com%2Fblog%2Fthe-best-tie-knot-for-your-headshot%2F&tbnid=f0mePlVDhAIxNM&vet=12ahUKEwihs4-86o_rAhVV454KHSFmCCIQMygOegUIARDuAQ..i&docid=UobcMAJU5BRp9M&w=1710&h=1140&q=head%20shot&ved=2ahUKEwihs4-86o_rAhVV454KHSFmCCIQMygOegUIARDuAQ')
Dana_Pine = User(first_name='Dana', last_name="Pine", image_url='https://www.google.com/imgres?imgurl=https%3A%2F%2Fimages.squarespace-cdn.com%2Fcontent%2Fv1%2F513aacf4e4b0abff73b93917%2F1476901462774-16NOFQRO62SZB63ZCM8A%2Fke17ZwdGBToddI8pDm48kOggE0Ch6pMGalwtLMqzsSB7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1Ufo5RWkg_J4of0jUNHaDHx6pZKBvpVYzidBWCapg0tuoMuEaB2HPGSYDV-11UTcW2g%2Fmorgan-hs-001.jpg%3Fformat%3D2500w&imgrefurl=https%3A%2F%2Fjoshuaaaronphotography.com%2Fheadshots-professional-business-portraits&tbnid=TWu_wg98Clz2iM&vet=12ahUKEwihs4-86o_rAhVV454KHSFmCCIQMygBegUIARDUAQ..i&docid=QMLqjQ4FXs_7hM&w=1920&h=1280&q=head%20shot&ved=2ahUKEwihs4-86o_rAhVV454KHSFmCCIQMygBegUIARDUAQ')
Mark_Thompson = User(first_name='Mark', last_name="Thompson", image_url='https://www.google.com/imgres?imgurl=https%3A%2F%2Fi.pinimg.com%2Foriginals%2Fe3%2F7e%2F0e%2Fe37e0e25686c2139b281a57a5b4906f2.jpg&imgrefurl=https%3A%2F%2Fwww.pinterest.com%2Fpin%2F460704236854562822%2F&tbnid=GBQUgulcaGKMqM&vet=12ahUKEwihs4-86o_rAhVV454KHSFmCCIQMygDegUIARDYAQ..i&docid=ggzHqVML9AbjqM&w=3744&h=5616&q=head%20shot&ved=2ahUKEwihs4-86o_rAhVV454KHSFmCCIQMygDegUIARDYAQ')



db.session.add(Dave_Allen)
db.session.add(Dana_Pine)
db.session.add(Mark_Thompson)


db.session.commit()
