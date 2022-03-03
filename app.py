from flask import Flask, request, make_response, session, abort
from flask import render_template, redirect, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/main")
def main_page():
    return render_template('main_content.html', title='TheLastWolfpack')


def main():
    app.run()


if __name__ == '__main__':
    main()
