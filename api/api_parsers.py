from flask_restful import reqparse

# парсер для получения капитана
get_cap_parser = reqparse.RequestParser()
get_cap_parser.add_argument('cap_name')
get_cap_parser.add_argument('extension_data', type=bool)

# парсер для получения исторической справки
get_hist_reference_parser = reqparse.RequestParser()

# парсер для получения исторической справки
get_uboat_parser = reqparse.RequestParser()
get_uboat_parser.add_argument('uboat_num')
get_cap_parser.add_argument('extension_data', type=bool)

# парсер для получения справки по типам лодок
get_uboat_types_parser = reqparse.RequestParser()

# парсер для работы с пользователем
user_put_parser = reqparse.RequestParser()
user_put_parser.add_argument('username')
user_put_parser.add_argument('email')
user_put_parser.add_argument('profile_picture')
user_put_parser.add_argument('fav_caps')
user_put_parser.add_argument('fav_boats')
user_put_parser.add_argument('msg')
user_put_parser.add_argument('attachment')
user_put_parser.add_argument('att_extension')
user_put_parser.add_argument('add_fav', type=int)

# парсер для создания пользователя
user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('username', required=True)
user_post_parser.add_argument('email', required=True)
user_post_parser.add_argument('password', required=True)
user_post_parser.add_argument('role', required=True)

# пасрер для создания сообщения
msg_parser = reqparse.RequestParser()
msg_parser.add_argument('text', required=True)
msg_parser.add_argument('attachment')

# парсер для получения сообщений
msg_get = reqparse.RequestParser()
msg_get.add_argument('last_msgs')