from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.uboats import Uboat


def abort_if_uboat_not_found(uboat_num):
    """Функция, проверяющая существование лодки с tactical_number={uboat_num}"""
    session = db_session.create_session()
    uboat = session.query(Uboat).filter(Uboat.tactical_number == uboat_num).first()
    if not uboat:
        abort(404, message=f"Uboat {uboat_num} not found")


class UboatResource(Resource):
    """Класс ресурса для одной лодки"""
    def get(self, uboat_num):
        """Метод получения лодки по тактическому номеру"""
        abort_if_uboat_not_found(uboat_num)
        session = db_session.create_session()
        uboat = session.query(Uboat).filter(Uboat.tactical_number == uboat_num).first()
        return jsonify({'uboat': uboat.to_dict(only=('id', 'tactical_number', 'ordered', 'launched', 'commissioned', 'commanders', 'career', 'successes', 'fate', 'coords'))})


class UboatListResource(Resource):
    """Класс ресурса для списка лодок"""
    def get(self):
        """Метод получения всех лодок"""
        session = db_session.create_session()
        uboats = session.query(Uboat).all()
        return jsonify({'uboats': [item.to_dict(only=(
            'id', 'tactical_number', 'ordered', 'launched', 'commissioned',
            'commanders', 'career', 'successes', 'fate', 'coords'))
            for item in uboats]})
