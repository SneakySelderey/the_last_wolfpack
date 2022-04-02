from flask_restful import reqparse

get_cap_parser = reqparse.RequestParser()
get_cap_parser.add_argument('cap_name')
