from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, \
    EmailField, BooleanField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Login / Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Password again', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    picture = FileField('Profile picture')
    username = StringField('Username')
    email = EmailField('Email')
    submit = SubmitField('Save')