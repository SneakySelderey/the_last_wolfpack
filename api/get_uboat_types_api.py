from flask import jsonify
from flask_restful import Resource, abort
import requests
from bs4 import BeautifulSoup


def abort_if_page_not_found():
    """Функция, проверяющая существование страницы со справкой по типам лодок"""
    response = requests.get("https://the-last-wolfpack.herokuapp.com/uboat_types")
    if response.status_code != 200:
        abort(404, message=f"Page https://the-last-wolfpack.herokuapp.com/uboat_types not found")


class UboatTypesResource(Resource):
    """Класс ресурса для страницы со справкой по типам лодок"""
    def get(self):
        """Метод получения страницы со справкой по типам лодок"""
        abort_if_page_not_found()
        response = requests.get("https://the-last-wolfpack.herokuapp.com/uboat_types")
        soup = BeautifulSoup(response.content, 'lxml')
        tags = soup.find_all(('p', 'li'))
        text = ''
        for i in tags[4:]:
            text += i.text
        return jsonify({'text': text, 'pics': ('https://the-last-wolfpack.herokuapp.com/static/img/misc.%20pictures/uboat_type_II.jpg',
                        'https://the-last-wolfpack.herokuapp.com/static/img/misc.%20pictures/uboat_type_VII.jpg',
                        'https://the-last-wolfpack.herokuapp.com/static/img/misc.%20pictures/uboat_type_IX.jpg',
                        'https://the-last-wolfpack.herokuapp.com/static/img/misc.%20pictures/uboat_type_XXI.jpg',
                        'https://the-last-wolfpack.herokuapp.com/static/img/misc.%20pictures/proj641.png',
                        'https://the-last-wolfpack.herokuapp.com/static/img/misc.%20pictures/proj675.png',
                        'https://the-last-wolfpack.herokuapp.com/static/img/misc.%20pictures/uss-clamagore.jpg')})
