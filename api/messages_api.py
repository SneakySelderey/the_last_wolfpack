from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.messages import Message
from api.api_parsers import msg_parser
import logging
import json


def abort_if_message_not_found(msg_id):
    """Функция, проверяющая существование сообщения с id={user_id}"""
    session = db_session.create_session()
    user = session.query(Message).get(msg_id)
    if not user:
        abort(404, message=f"Message {msg_id} not found")


class MessagesResource(Resource):
    """Класс ресурса для одного сообщения"""
    def get(self, msg_id):
        """Метод получения сообщения по id"""
        abort_if_message_not_found(msg_id)
        session = db_session.create_session()
        msg = session.query(Message).get(msg_id)
        data = msg.to_dict()
        data['user'] = msg.user.to_dict(only=(
            'id', 'username', 'email', 'register_date',
            'profile_picture'))
        logging.info(f'GET message {msg_id} -> success')
        return jsonify({'message': data})

    def delete(self, msg_id):
        """Метод удаления сообщения по id"""
        abort_if_message_not_found(msg_id)
        session = db_session.create_session()
        msg = session.query(Message).get(msg_id)
        session.delete(msg)
        session.commit()
        logging.info(f'DELETE message {msg_id} -> success')
        return jsonify({'success': 'OK'})


class MessagesListResource(Resource):
    """Класс ресурса для списка сообщений"""
    def get(self):
        """Метод получения всех сообщений"""
        session = db_session.create_session()
        messages = session.query(Message).all()
        to_ret = []
        for i in messages:
            value = i.to_dict()
            value['user'] = i.user.to_dict(only=(
                'id', 'username', 'email', 'register_date',
                'profile_picture'))
            to_ret.append(value)
        logging.info('GET messages -> success')
        return jsonify({'messages': to_ret})

    def post(self):
        """Метод для добавления сообщения"""
        args = msg_parser.parse_args()
        session = db_session.create_session()
        msg = Message()
        msg.text = args['text']
        session.add(msg)
        session.commit()
        logging.info(f'POST message -> success')
        return jsonify({'success': 'OK'})