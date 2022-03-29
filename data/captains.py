import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Captain(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Класс таблицы для капитана в БД"""
    __tablename__ = 'caps'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    image = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    boats = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    profile_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)