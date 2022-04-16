import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


association_table_1 = sqlalchemy.Table(
    'users_to_captains',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('captains', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('caps.name'))
)


association_table_2 = sqlalchemy.Table(
    'users_to_boats',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('boats', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('uboats.tactical_number'))
)


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Класс таблицы для пользователя в БД"""
    __tablename__ = 'users'
    serialize_rules = ('-fav_caps', '-fav_boats')
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    register_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.now)
    profile_picture = sqlalchemy.Column(sqlalchemy.String,
                                        default='empty_pic.png')
    fav_caps = orm.relation("Captain",
                            secondary="users_to_captains", backref="users")
    fav_boats = orm.relation("Uboat", secondary="users_to_boats",
                             backref="users")
    messages = orm.relation("Message", back_populates='user')

    def set_password(self, password):
        """Функция установки хешированного пароля.
        Принимает пароль (строку)"""
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        """Функция проверки введенного пароля с тем, который записан в БД.
        Принимает пароль (строку)"""
        return check_password_hash(self.hashed_password, password)