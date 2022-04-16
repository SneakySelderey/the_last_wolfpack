import sqlalchemy
from datetime import datetime

from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


def get_time():
    return datetime.now().strftime('%d %b')


class Message(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Класс для сообщения в БД"""
    __tablename__ = 'messages'
    serialize_rules = ('-user',)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    from_user = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('users.id'))
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.Date, default=get_time)
    user = orm.relation('User')