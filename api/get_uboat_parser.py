from flask_restful import reqparse

get_uboat_parser = reqparse.RequestParser()
get_uboat_parser.add_argument('uboat_num')
