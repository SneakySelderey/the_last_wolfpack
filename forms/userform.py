from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, \
    EmailField, BooleanField, FileField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    """Класс формы регистрации нового пользователя"""
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Login / Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'password_again')])
    password_again = PasswordField('Password again', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    """Класс формы авторизации пользователя"""
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    """Класс формы редактирования профиля пользователя"""
    picture = FileField('Profile picture')
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Save')