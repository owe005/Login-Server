from app import app, conn, get_user
import flask
from flask import request, render_template
import hashlib
import uuid

from forms.register_form import RegisterForm

@app.route('/register', methods=['GET', 'POST'])

def register():
    form = RegisterForm()

    if form.is_submitted():
        print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
        print(request.form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        c = conn.execute("SELECT * FROM users WHERE username GLOB ?", (username,))
        row = c.fetchone()
        salt = str(uuid.uuid4())
        hasher = hashlib.sha512()
        hasher.update(password.encode())
        hasher.update(salt.encode())
        password_hash = hasher.hexdigest()
        conn.execute("INSERT INTO users (username, password_hash, salt) values (?, ?, ?);", (username, password_hash, salt))
        user = get_user(username)

        return flask.redirect('/')

    return render_template('./register.html', form=form)
