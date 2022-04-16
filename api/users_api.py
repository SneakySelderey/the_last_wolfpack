from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.captains import Captain
from data.uboats import Uboat
from data.user import User
from data.messages import Message
from api.api_parsers import user_put_parser, user_post_parser
import logging


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
        logging.info(f'GET user {user.username} -> success')
        return jsonify({'user': user.to_dict(only=(
            'id', 'username', 'email', 'register_date',
            'profile_picture'))})

    def delete(self, user_id):
        """Метод удаления польователя по id"""
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        logging.info(f'DELETE user {user.username} -> success')
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        """Метод изменения данных пользоавтеля по id"""
        abort_if_user_not_found(user_id)
        args = user_put_parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        # Изменение обычных значений
        changed = {j: args[j] for j in user.__dict__ if args.get(
            j, None) is not None and j not in ['fav_caps', 'fav_boats',
                                               'add_fav', 'msg']}
        for i in changed:
            setattr(user, i, changed[i])
        # Изменение (добавление или удаление) особых значений: капитанов и
        # лодок
        fav_caps = args.get('fav_caps', [])
        fav_boats = args.get('fav_boats', [])
        if fav_caps:
            put_caps = session.query(Captain).filter(Captain.name.in_(
                fav_caps.split(','))).all()
            if args.get('add_fav'):
                for i in put_caps:
                    user.fav_caps.append(i)
            else:
                for i in put_caps:
                    user.fav_caps.remove(i)
        if fav_boats:
            put_boats = session.query(Uboat).filter(Uboat.tactical_number.in_(
                fav_boats.split(','))).all()
            if args.get('add_fav'):
                for i in put_boats:
                    user.fav_boats.append(i)
            else:
                for i in put_boats:
                    user.fav_boats.remove(i)
        if args.get('msg', False):
            # Добавление сообщения
            msg = Message()
            msg.text = args['msg']
            user.messages.append(msg)
        session.commit()
        logging.info(f'PUT user {user.username} -> success')
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    """Класс ресурса для списка пользователей"""
    def get(self):
        """Метод получения всех пользователей"""
        session = db_session.create_session()
        users = session.query(User).all()
        logging.info('GET users -> success')
        return jsonify({'users': [item.to_dict(only=(
            'id', 'username', 'email', 'register_date',
            'profile_picture')) for item in users]})

    def post(self):
        """Метод для добавления пользователя"""
        args = user_post_parser.parse_args()
        session = db_session.create_session()
        user = User()
        user.username = args['username']
        user.email = args['email']
        user.role = args['role']
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        logging.info(f'POST user {user.username} -> success')
        return jsonify({'success': 'OK'})
