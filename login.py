from app import app, get_user, user_loader
import flask
from flask import request, render_template
import flask_login
from flask_login import login_user, login_required
import hashlib

from forms.login_form import LoginForm

def check_password(password, salt, pass_hash):
    hash = hashlib.sha512()
    hash.update(password.encode())
    hash.update(salt.encode())
    computed_hash = hash.hexdigest()
    return computed_hash == pass_hash


def get_current_user():
    id = flask_login.current_user.get_id()
    if id:
        user = user_loader(id)

    else:
        user = {"id": 0, "username": "Anonymous"}

    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.is_submitted():
        print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
        print(request.form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = get_user(username)

        if user and check_password(password, user.get("salt"), user.get("hash")):
            user = user_loader(user.get("id"))
            login_user(user)
            next = flask.request.args.get('next')
            return flask.redirect(next or flask.url_for('index'))

    return render_template('./login.html', form=form)

@app.route("/logout")
@login_required

def logout():
    flask_login.logout_user()
    return flask.redirect("/")
