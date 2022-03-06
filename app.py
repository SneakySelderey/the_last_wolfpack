import os
from flask import Flask, request, make_response, session, abort
from flask import render_template, redirect, jsonify
from data import db_session
from data.captains import Captain

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def main_page():
    return render_template('main_content.html', title='TheLastWolfpack')


@app.route("/captains")
def captains_list():
    db_sess = db_session.create_session()
    caps = db_sess.query(Captain).all()
    return render_template('caps_list.html', title='Капитаны Кригсмарине', caps=caps)


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    db_session.global_init("db/database.db")
    main()
