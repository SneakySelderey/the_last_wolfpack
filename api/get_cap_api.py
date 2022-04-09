import logging
from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.captains import Captain


def abort_if_cap_not_found(cap_name):
    """Функция, проверяющая существование капитана с name={cap_name}"""
    session = db_session.create_session()
    cap = session.query(Captain).filter(Captain.name == cap_name).first()
    if not cap:
        abort(404, message=f"Captain {cap_name} not found")


class CapResource(Resource):
    """Класс ресурса для одного капитана"""
    def get(self, cap_name):
        """Метод получения капитана по имени"""
        abort_if_cap_not_found(cap_name)
        session = db_session.create_session()
        cap = session.query(Captain).filter(Captain.name == cap_name).first()
        cap.image = f'https://the-last-wolfpack.herokuapp.com//static/img/{cap.id - 1}.png'
        logging.info(f'GET captain {cap_name} -> success')
        return jsonify({'captain': cap.to_dict(only=('id', 'image', 'profile_link', 'name', 'info', 'boats'))})


class CapListResource(Resource):
    """Класс ресурса для списка капитанов"""
    def get(self):
        """Метод получения всех капитанов"""
        session = db_session.create_session()
        captains = session.query(Captain).all()
        logging.info('GET captains -> success')
        caps = []
        for item in captains:
            item.image = f'https://the-last-wolfpack.herokuapp.com//static/img/{item.id - 1}.png'
            caps.append(item.to_dict(only=('id', 'image', 'name',
                                               'info', 'boats', 'profile_link')))
        return jsonify({'captains': caps})
