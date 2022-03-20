import os
import os.path
from flask import Flask, request, make_response, session, abort, url_for, redirect
from flask import render_template, redirect, jsonify
from flask_login import LoginManager, logout_user, login_required, login_user, \
    current_user
from data.user import User
from data.captains import Captain
from data import db_session
from forms.userform import LoginForm, RegisterForm, EditProfileForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def main_page():
    return redirect('/captains')
    return redirect('/historical_reference')


@app.route("/historical_reference")
def historical_reference():
    return render_template('historical_reference.html', title='Историческая справка')


@app.route("/captains")
def captains_list():
    db_sess = db_session.create_session()
    caps = db_sess.query(Captain).all()

    count = 0
    for i in caps:
        if i.image:
            name = f'{count}.png'
            with open(f'static/img/{name}', 'wb') as f:
                f.write(i.image)
        count += 1

    return render_template('caps_list.html', title='Капитаны Кригсмарине',
                           caps=caps)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
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
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/profile")
        return render_template('login.html',
                               message="Wrong login or password",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/profile')
@login_required
def user_profile():
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    return render_template('profile.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    db_sess = db_session.create_session()
    if request.method == 'GET':
        user = db_sess.query(User).get(current_user.id)
        form.username.data = user.username
    if form.validate_on_submit():
        user = db_sess.query(User).get(current_user.id)
        if db_sess.query(User).filter(User.username == form.username.data) \
            and not form.username.data == current_user.username:
            return render_template('edit_profile.html',
                                   message='Username is already taken',
                                   form=form)
        user.username = form.username.data
        if form.picture.data:
            image_data = request.files[form.picture.name]
            name = os.path.join('static/img/profile_pictures',
                                current_user.username + '.png')
            open(name, 'wb').write(image_data.read())
            user.profile_picture = current_user.username + '.png'
        db_sess.commit()
        return redirect("/profile")
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


if __name__ == '__main__':
    db_session.global_init("database.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)