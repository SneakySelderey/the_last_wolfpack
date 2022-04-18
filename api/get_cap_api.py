import logging
from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.captains import Captain
from api.api_parsers import get_cap_parser, put_cap_parser, post_cap_parser


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
        args = get_cap_parser.parse_args()
        session = db_session.create_session()
        cap = session.query(Captain).filter(Captain.name == cap_name).first()
        logging.info(f'GET captain {cap_name} -> success')
        if args.get('extension_data', False):
            data = {'captain': cap.to_dict(
                only=('id', 'profile_link', 'name', 'info', 'boats', 'users',
                      'orm_boats'))}
        else:
            data = {'captain': cap.to_dict(only=('id', 'profile_link', 'name', 'info', 'boats'))}
        data['captain']['image'] = f'https://the-last-wolfpack.herokuapp.com//static/img/{cap.id - 1}.png'
        return jsonify(data)

    def delete(self, cap_name):
        """Метод удаления капитана по имени"""
        abort_if_cap_not_found(cap_name)
        session = db_session.create_session()
        cap = session.query(Captain).filter(Captain.name == cap_name).first()
        logging.info(f'DELETE captain {cap_name} -> success')
        session.delete(cap)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, cap_name):
        """Метод изменения капитана по имени"""
        abort_if_cap_not_found(cap_name)
        args = put_cap_parser.parse_args()
        session = db_session.create_session()
        cap = session.query(Captain).filter(Captain.name == cap_name).first()
        changed = {j: args[j] for j in cap.__dict__ if args.get(
            j, None) is not None}
        for i in changed:
            setattr(cap, i, changed[i])
        session.commit()
        return jsonify({'success': 'OK'})


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

    def post(self):
        """Метод для добавления капитана"""
        args = post_cap_parser.parse_args()
        session = db_session.create_session()
        cap = Captain()
        cap.name = args['name']
        cap.info = args['info']
        cap.boats = args['boats']
        cap.profile_link = args['profile_link']
        session.add(cap)
        session.commit()
