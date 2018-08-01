from flask_wtf import Form
from wtforms import validators,StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField


class RegisterForm(Form):
    fullname = StringField('Fullname', [validators.Required()] )
    email = EmailField('Email',[validators.Required()] )
    username = StringField('Username', [
                validators.Required(),
                validators.Length(min=2, max=30)
                ])
    password = PasswordField('New Password', [
                validators.Required(),
                validators.Length(min=8, max=80),
                validators.EqualTo('confirm',
                message="Password don't match")
                ])
    confirm = PasswordField('Repeat Password')
    is_author = BooleanField('Author?')
    is_admin = BooleanField('Admin?')


class LoginForm(Form):
    username = StringField('Username', [validators.Required()] )
    password = PasswordField('Password', [validators.Required()] )

class ChangePasswordForm(Form):
    oldpassword = PasswordField('Old Password', [validators.Required()])
    newpassword = PasswordField('New Password', [
                        validators.Required(),
                        validators.Length(min=8, max=30),
                        validators.EqualTo('confirm', message="Passwords don't match")
                        ])
    confirm = PasswordField('Confirm new Password', [validators.Required()])
