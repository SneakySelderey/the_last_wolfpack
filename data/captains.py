import sqlalchemy
from sqlalchemy import orm
import base64
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.types import VARCHAR
from sqlalchemy import func


class ImageColumn(VARCHAR):
    """Класс для столбца таблицы с изорбражением. Создан с целью избежания
    ошибки декодирования"""

    def column_expression(self, col):
        return func.HEX(col)


class CapsToBoats(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'captains_to_uboats'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    captains = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey(
        'caps.name'))
    uboats = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey(
        'uboats.tactical_number'))
    captain = orm.relation('Captain', back_populates='orm_boats')
    boat = orm.relation('Uboat', back_populates="orm_captains")
    commissioned = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    period = sqlalchemy.Column(sqlalchemy.String, nullable=True)


class Captain(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Класс таблицы для капитана в БД"""
    __tablename__ = 'caps'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    image = sqlalchemy.Column(ImageColumn, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    boats = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    profile_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    orm_boats = orm.relation("CapsToBoats", back_populates="captain")