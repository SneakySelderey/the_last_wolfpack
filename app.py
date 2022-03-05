import os
from flask import Flask, request, make_response, session, abort
from flask import render_template, redirect, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/main")
def main_page():
    return render_template('main_content.html', title='TheLastWolfpack')


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
