from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.user import User


def abort_if_user_not_found(user_id):
    """Функция, проверяющая существование пользователя с id={user_id}"""
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    """Класс ресурса для одного пользователя"""
    def get(self, user_id):
        """Метод получения пользователя по id"""
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict()})

    def delete(self, user_id):
        """Метод удаления польователя по id"""
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    """Класс ресурса для списка пользователей"""
    def get(self):
        """Метод получения всех пользователей"""
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict() for item in users]})