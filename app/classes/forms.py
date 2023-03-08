# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

from flask_wtf import FlaskForm
import mongoengine.errors
from wtforms.validators import URL, Email, DataRequired
from wtforms.fields.html5 import URLField
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, FileField, BooleanField

class ProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    submit = SubmitField('Post')
    role = SelectField("Role",choices=[("CEO","CEO"),("Senior Manager","Senior Manager"),("Senior Executive Chief Assistant Officer of Strategy","Senior Executive Chief Assistant Officer of Strategy")])

class FarmForm(FlaskForm):
    zipCode = StringField()
    streetAddress = StringField()
    city = StringField()
    state = StringField()
    type = SelectField("Type", choices=[("Farmer's Market","Farmer's Market"), ("Animal Farm","Animal Farm"), ("Grocery Store","Grocery Store"), ("Vegetable Farm", "Vegetable Farm"), ("Food Bank", "Food Bank")])
    picture = FileField()
    price = SelectField("Price", choices=[("Free", "Free"), ("$","$"), ("$$", "$$"), ("$$$", "$$$")])
    name = StringField()
    submit = SubmitField('Cultivate')

class BlogForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Blog', validators=[DataRequired()])
    tag = StringField('Tag', validators=[DataRequired()])
    submit = SubmitField('Blog')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')
