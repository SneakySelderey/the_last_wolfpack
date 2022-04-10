from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.uboats import Uboat
from api.api_parsers import get_uboat_parser
import logging
import json


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
        args = get_uboat_parser.parse_args()
        session = db_session.create_session()
        uboat = session.query(Uboat).filter(
            Uboat.tactical_number == uboat_num).first()
        logging.info(f'GET uboat {uboat_num} -> success')
        if args.get('extension_data', False):
            return jsonify({'uboat': uboat.to_dict()})
        return jsonify({'uboat': uboat.to_dict(only=(
            'id', 'tactical_number', 'ordered', 'laid_down', 'launched',
            'commissioned', 'commanders', 'career', 'successes', 'fate',
            'coords'))})


class UboatListResource(Resource):
    """Класс ресурса для списка лодок"""
    def get(self):
        """Метод получения всех лодок"""
        session = db_session.create_session()
        uboats = session.query(Uboat).all()
        logging.info('GET uboats -> success')
        return jsonify({'uboats': [item.to_dict(only=(
            'id', 'tactical_number', 'ordered', 'launched', 'commissioned',
            'commanders', 'career', 'successes', 'fate', 'coords'))
            for item in uboats]})


class CapsBoatsRelationship(Resource):
    """Класс ресурса для json-файла, в котором записаны отношения капитанов и
    лодок"""
    def get(self):
        with open('api/caps_boats.json') as file:
            return jsonify(json.load(file))
