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
        return jsonify({'captain': cap.to_dict(only=('id', 'image', 'profile_link', 'name', 'info', 'boats'))})


class CapListResource(Resource):
    """Класс ресурса для списка капитанов"""
    def get(self):
        """Метод получения всех капитанов"""
        session = db_session.create_session()
        captains = session.query(Captain).all()
        return jsonify({'captains': [item.to_dict(only=(
            'id', 'name', 'info', 'boats', 'profile_link')) for
                item in captains]})
