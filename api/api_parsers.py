from flask_restful import reqparse

# парсер для получения капитана
get_cap_parser = reqparse.RequestParser()
get_cap_parser.add_argument('cap_name')

# парсер для получения исторической справки
get_hist_reference_parser = reqparse.RequestParser()

# парсер для получения исторической справки
get_uboat_parser = reqparse.RequestParser()
get_uboat_parser.add_argument('uboat_num')

# парсер для получения справки по типам лодок
get_uboat_types_parser = reqparse.RequestParser()

# парсер для работы с пользователем
user_put_parser = reqparse.RequestParser()
user_put_parser.add_argument('username')
user_put_parser.add_argument('email')
user_put_parser.add_argument('profile_picture')
user_put_parser.add_argument('fav_caps')
user_put_parser.add_argument('fav_boats')
user_put_parser.add_argument('add_fav', type=int)
