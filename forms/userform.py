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
            message = f'Длина пароля должна быть между {min_l} и {max_l} символами'
        else:
            message = f'Пароль должен состоять как минимум из {min_l} символов'

    def _length(form, field):
        len_s = field.data and len(field.data) or 0
        if len_s < min_l or max_l != -1 and len_s > max_l:
            raise ValidationError(message)

    return _length


def letters(message=None):
    """Валидатор для проверки наличия букв в пароле"""
    if not message:
        message = 'Должна быть как минимум одна буква'

    def _letters(form, field):
        if not any(x.isalpha() for x in field.data):
            raise ValidationError(message)

    return _letters


def digits(message=None):
    """Валидатор для проверки наличия цифр в пароле"""
    if not message:
        message = 'Должна быть как минимум одна цифра'

    def _digits(form, field):
        if not any(x.isdigit() for x in field.data):
            raise ValidationError(message)

    return _digits


def extension(*extensions, message=None):
    """Валидатор для проверки расширения файла"""
    if not message:
        message = 'Недопустимое расширение файла'

    def _extension(form, field):
        if field.data is not None:
            filename = secure_filename(field.data.filename)
            if not any(filename.endswith(x) for x in extensions):
                raise ValidationError(message)

    return _extension


class RegisterForm(FlaskForm):
    """Класс формы регистрации нового пользователя"""
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Логин (почта)', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[
        DataRequired(), length(min_l=8), letters(), digits()])
    password_again = PasswordField('Повторите пароль', validators=[
        DataRequired(), EqualTo('password', message='Пароли на совпадают')])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    """Класс формы авторизации пользователя"""
    email = EmailField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class EditProfileForm(FlaskForm):
    """Класс формы редактирования профиля пользователя"""
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    picture = FileField('Фото профиля', validators=[
        extension('.png', '.jpg', '.jpeg')])
    submit = SubmitField('Сохранить')