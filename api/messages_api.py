from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.messages import Message
from api.api_parsers import msg_parser
import logging


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
        logging.info(f'GET message {msg_id} -> success')
        return jsonify({'message': msg.to_dict()})

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
        logging.info('GET messages -> success')
        return jsonify({'messages': [item.to_dict() for item in messages]})

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