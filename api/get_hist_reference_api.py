from flask import jsonify
from flask_restful import Resource, abort
import requests
from bs4 import BeautifulSoup


def abort_if_page_not_found():
    """Функция, проверяющая существование страницы с исторической справкой"""
    response = requests.get("https://the-last-wolfpack.herokuapp.com/historical_reference")
    if response.status_code != 200:
        abort(404, message=f"Page https://the-last-wolfpack.herokuapp.com/historical_reference not found")


class HistRefResource(Resource):
    """Класс ресурса для страницы с исторической справкой"""
    def get(self):
        """Метод получения страницы с исторической справкой"""
        abort_if_page_not_found()
        response = requests.get("https://the-last-wolfpack.herokuapp.com/historical_reference")
        soup = BeautifulSoup(response.content, 'lxml')
        tags = soup.find_all(('p', 'li'))
        text = ''
        for i in tags:
            text += i.text
        return jsonify({'text': text, 'pics': ('https://the-last-wolfpack.herokuapp.com/static/img/misc.%20pictures/U-96.jpg',
                        'https://the-last-wolfpack.herokuapp.com/static/img/misc.%20pictures/Karl_Doenitz.jpg',
                        'https://the-last-wolfpack.herokuapp.com/static/img/misc.%20pictures/U-243_under_attack.jpg',
                        'https://the-last-wolfpack.herokuapp.com/static/img/misc.%20pictures/convoy.jpg')})
