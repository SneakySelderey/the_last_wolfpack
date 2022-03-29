from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import PasswordField, StringField, SubmitField, \
    EmailField, BooleanField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, EqualTo, ValidationError


def length(min_l=-1, max_l=-1, message=None):
    """Валидатор для проверки длины пароля"""
    if not message:
        if max_l != -1:
            message = f'Must be between {min_l} and {max_l} characters long.'
        else:
            message = f'Must be at least {min_l} characters'

    def _length(form, field):
        len_s = field.data and len(field.data) or 0
        if len_s < min_l or max_l != -1 and len_s > max_l:
            raise ValidationError(message)

    return _length


def letters(message=None):
    """Валидатор для проверки наличия букв в пароле"""
    if not message:
        message = 'Must be at least one letter'

    def _letters(form, field):
        if not any(x.isalpha() for x in field.data):
            raise ValidationError(message)

    return _letters


def digits(message=None):
    """Валидатор для проверки наличия цифр в пароле"""
    if not message:
        message = 'Must be at least one digit'

    def _digits(form, field):
        if not any(x.isdigit() for x in field.data):
            raise ValidationError(message)

    return _digits


def extension(*extensions, message=None):
    """Валидатор для проверки расширения файла"""
    if not message:
        message = 'Invalid extension file'

    def _extension(form, field):
        filename = secure_filename(field.data.filename)
        if not any(filename.endswith(x) for x in extensions):
            raise ValidationError(message)

    return _extension


class RegisterForm(FlaskForm):
    """Класс формы регистрации нового пользователя"""
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Login / Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(), length(min_l=8), letters(), digits()])
    password_again = PasswordField('Password again', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    """Класс формы авторизации пользователя"""
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    """Класс формы редактирования профиля пользователя"""
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    picture = FileField('Profile picture', validators=[
        extension('.png', '.jpg', '.jpeg')])
    submit = SubmitField('Save')