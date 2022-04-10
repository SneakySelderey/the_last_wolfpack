import os.path
from flask import Flask, request
from flask import render_template, redirect
from flask_login import LoginManager, logout_user, login_required, login_user,\
    current_user
from flask_restful import Api
from werkzeug.utils import secure_filename
from api import users_api, get_cap_api, get_uboat_api, get_hist_reference_api, get_uboat_types_api
from data.user import User
from data.captains import Captain
from data.uboats import Uboat
from data import db_session
from forms.userform import LoginForm, RegisterForm, EditProfileForm
from forms.DB_update_form import UpdateForm
import logging
import DB_updater
from requests import put, post, get
from decouple import config
import discord_bot
from threading import Thread
import socket


app = Flask(__name__)
app.config['SECRET_KEY'] = config('FLASK_SECRET_KEY', default='not found')
api = Api(app)
api.add_resource(users_api.UsersResource, '/api/users/<int:user_id>')
api.add_resource(users_api.UsersListResource, '/api/users')
api.add_resource(get_cap_api.CapResource, '/api/caps/<string:cap_name>')
api.add_resource(get_cap_api.CapListResource, '/api/caps')
api.add_resource(get_uboat_api.UboatResource, '/api/uboats/<string:uboat_num>')
api.add_resource(get_uboat_api.UboatListResource, '/api/uboats')
api.add_resource(get_uboat_api.CapsBoatsRelationship, '/api/rel')
api.add_resource(get_hist_reference_api.HistRefResource, '/api/hist_ref')
api.add_resource(get_uboat_types_api.UboatTypesResource, '/api/uboat_types')
login_manager = LoginManager()
login_manager.init_app(app)
# logging.getLogger('werkzeug').disabled = True
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)


@app.route("/")
def main_page():
    """Основная страница"""
    return render_template('main_content.html', title='The Last Wolfpack')


@app.route("/uboat_types")
def uboat_types():
    """Страница с типами лодок"""
    return render_template('uboat_types.html',
                           title='Типы подводных лодок Кригсмарине')


@app.route("/historical_reference")
def historical_reference():
    """Страница с исторической справкой"""
    return render_template('historical_reference.html',
                           title='Историческая справка')


@app.route("/captains", methods=['GET', 'PUT', 'POST'])
def captains_list():
    """Страница с капитанами"""
    form = UpdateForm()
    db_sess = db_session.create_session()
    caps = db_sess.query(Captain).all()
    if current_user.is_authenticated:
        fav_caps = db_sess.query(User).get(current_user.id).fav_caps
    else:
        fav_caps = []
    if form.validate_on_submit():
        DB_updater.run()

    return render_template('caps_list.html', title='Капитаны Кригсмарине',
                           caps=caps, form=form, fav_caps=fav_caps)


@app.route("/uboats", methods=['GET', 'POST', 'PUT'])
def uboats_list():
    """Страница с лодками"""
    form = UpdateForm()
    data = get(f'http://{request.host}/api/rel').json()
    db_sess = db_session.create_session()
    uboats = db_sess.query(Uboat).all()
    caps = get(f'http://{request.host}/api/caps').json()
    caps_id_name = {i['id']: i['name'] for i in caps['captains']}
    if current_user.is_authenticated:
        fav_boats = db_sess.query(User).get(current_user.id).fav_boats
    else:
        fav_boats = []
    if form.validate_on_submit():
        DB_updater.run()
    return render_template('uboats_list.html', title='Подлодки Кригсмарине',
                           uboats=uboats, fav_boats=fav_boats, form=form,
                           rel=data, caps=caps_id_name)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации и обработка формы"""
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register',
                                   form=form,
                                   message="Passwords don't match")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register',
                                   form=form,
                                   message="User is already exists")
        if db_sess.query(User).filter(
                User.username == form.username.data).first():
            return render_template('register.html', title='Register',
                                   form=form,
                                   message="User is already exists")
        args = {'username': form.username.data, 'email': form.email.data,
                'password': form.password.data}
        try:
            post(f'http://{request.host}/api/users', json=args)
            app.logger.info(f'{form.username.data} registered successfully')
            return redirect('/login')
        except Exception as error:
            app.logger.error('User could not register. Reason:',
                             str(error).split('\n')[-1])
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница авторизации и обработки формы"""
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        try:
            user = db_sess.query(User).filter(
                User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                app.logger.info(f'{user.username} logged in successfully')
                return redirect("/profile")
            return render_template('login.html',
                                   message="Wrong login or password",
                                   form=form, title="Authorization")
        except Exception as error:
            app.logger.fatal('User could not login. Reason:',
                             str(error).split('\n')[-1])
    return render_template('login.html', title='Authorization', form=form)


@app.route('/logout')
@login_required
def logout():
    """Выход пользователя"""
    app.logger.info(f'{current_user.username} logged out successfully')
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    """Загрузка пользователя"""
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    """Страница профиля пользователя"""
    form = EditProfileForm()
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    fav_caps = user.fav_caps
    fav_boats = user.fav_boats
    if request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    if form.validate_on_submit():
        if db_sess.query(User).filter(
            User.email == form.email.data).first() and not \
                form.email.data == current_user.email:
            return render_template(
                'profile.html', message='Email is already taken',
                form=form, title='Profile', fav_caps=fav_caps,
                fav_boats=fav_boats)
        if db_sess.query(User).filter(
            User.username == form.username.data).first() and not \
                form.username.data == current_user.username:
            return render_template(
                'profile.html', message='Username is already taken',
                form=form, title='Profile', fav_caps=fav_caps,
                fav_boats=fav_boats)
        args = {'username': form.username.data, 'email': form.email.data}
        if form.picture.data is not None:
            filename = secure_filename(form.picture.data.filename)
            form.picture.data.save('static/img/profile_pictures/' + filename)
            args['profile_picture'] = filename
        try:
            put(f'http://{request.host}/api/users/{current_user.id}', json=args)
            db_sess.commit()
            app.logger.info(f'{user.username} changed his profile successfully')
            return redirect('/dummy')
        except Exception as error:
            app.logger.fatal('User could not edit profile. Reason:',
                             str(error).split('\n')[-1])
    return render_template('profile.html', user=user, title='Profile',
                           form=form, fav_caps=fav_caps, fav_boats=fav_boats)


@app.route('/dummy')
def dummy():
    return redirect('/profile')


def website_run():
    db_session.global_init("database.db")
    DB_updater.make_relations()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    website_thread = Thread(target=website_run)
    website_thread.start()
    discord_bot.run()
    website_thread.join()
