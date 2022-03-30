from flask_restful import reqparse

user_put_parser = reqparse.RequestParser()
user_put_parser.add_argument('username')
user_put_parser.add_argument('email')
user_put_parser.add_argument('profile_picture')
user_put_parser.add_argument('fav_caps', type=list)
user_put_parser.add_argument('fav_boats', type=list)
user_put_parser.add_argument('add_fav', type=bool)