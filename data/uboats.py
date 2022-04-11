import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Uboat(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Класс таблицы для лодки в БД"""
    __tablename__ = 'uboats'
    serialize_rules = ('-orm_captains',)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    tactical_number = sqlalchemy.Column(sqlalchemy.String)
    ordered = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    laid_down = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    launched = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    commissioned = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    commanders = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    career = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    successes = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    fate = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    coords = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    orm_captains = orm.relation("CapsToBoats", back_populates="boat")
