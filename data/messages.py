import sqlalchemy
from datetime import datetime
from sqlalchemy import orm, VARCHAR
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from random import getrandbits


class TextColumn(VARCHAR):
    """Класс для столбца таблицы с текстом сообщения. Нужен для правильного
    отображения сообщений на кирилице"""

    def column_expression(self, col):
        return col.decode('utf8')


class Message(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Класс для сообщения в БД"""
    __tablename__ = 'messages'
    serialize_rules = ('-user',)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    from_user = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('users.id'))
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    attachment = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.Date, default=datetime.now)
    user = orm.relation('User')

    def set_secret_hash(self, ext):
        """Установка хеша сообщения"""
        self.attachment = str(getrandbits(128)) + '.' + ext