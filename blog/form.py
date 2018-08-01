from flask_wtf import Form
from wtforms import StringField, validators, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from author.form import RegisterForm
from blog.models import MainCategory, SubCategory, SubSubCategory
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields.html5 import EmailField


class SetupForm(RegisterForm):
    title = StringField('Blog Title', [validators.Required(), validators.Length(min=2, max=80)])
    category1 = StringField('Category # 1', [validators.Required(), validators.Length(min=2, max=60)])
    category2 = StringField('Category # 2', [validators.Required(), validators.Length(min=2, max=60)])
    category3 = StringField('Category # 3', [validators.Required(), validators.Length(min=2, max=60)])

def maincategories():
    return MainCategory.query
def subcategories():
    return SubCategory.query
def subsubcategories():
    return SubSubCategory.query


class PostForm(Form):
    image = FileField('Image', validators = [FileAllowed(['jpg', 'png'], 'Only .jpg or .png files are allowed') ])
    title = StringField('Title', [validators.Required(), validators.Length(max=50)])
    body = TextAreaField('Content', [validators.Required()])
    keywords = StringField('Keywords divided with ","')
    maincategory = QuerySelectField('Maincategory', query_factory=maincategories, allow_blank=False)
    subcategory = QuerySelectField('Subcategory', query_factory=subcategories, allow_blank=True)
    new_subcategory = StringField('New Subcategory', [validators.Length(max=60)])
    subsubcategory = QuerySelectField('Sub-Subcategory', query_factory=subsubcategories, allow_blank=True)
    new_subsubcategory = StringField('New Sub-Subcategory', [validators.Length(max=60)])

class CommentForm(Form):
    name = StringField('Your Name', [validators.Required(), validators.Length(max=80)])
    email = EmailField('Your Email',[validators.Required(), validators.Length(max=80)] )
    body = TextAreaField('Your Comment', [validators.Required()])

class NewsletterForm(Form):
    re = StringField('Re:', [validators.Required(), validators.Length(max=100)])
    title = StringField('Heading', [validators.Required(), validators.Length(max=100)])
    body = TextAreaField('Message', [validators.Required()])
