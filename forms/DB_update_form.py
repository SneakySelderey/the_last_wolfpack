from flask_wtf import FlaskForm
from wtforms import SubmitField


class UpdateForm(FlaskForm):
    """Класс формы обновления БД"""
    submit = SubmitField('Обновить БД')
