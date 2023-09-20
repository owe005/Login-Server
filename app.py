from http import HTTPStatus
from flask import Flask, abort, send_from_directory, make_response, request
from werkzeug.datastructures import WWWAuthenticate
from base64 import b64decode
import sys
import apsw
from apsw import Error
from pygments.formatters import HtmlFormatter
from threading import local
from json import dumps
import flask_login
from flask_login import login_required

tls = local()
inject = "'; insert into messages (sender,message) values ('foo', 'bar');select '"
cssData = HtmlFormatter(nowrap=True).get_style_defs('.highlight')
conn = None

# Set up app
app = Flask(__name__)
# The secret key enables storing encrypted session data in a cookie (make a secure random key for this!)
app.secret_key = 'mY s3kritz'

# Add a login manager to the app
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Class to store user info
# UserMixin provides us with an `id` field and the necessary
# methods (`is_authenticated`, `is_active`, `is_anonymous` and `get_id()`)
class User(flask_login.UserMixin):
    def __init__(self, user_id):
        c = conn.execute("SELECT * FROM users WHERE id GLOB ?", (user_id,))
        row = c.fetchone()
        self.id = row[0]
        self.username = row[1]

# This method is called whenever the login manager needs to get
# the User object for a given user id
@login_manager.user_loader
def user_loader(user_id):
    user = User(user_id)
    return user

def get_user(username):
    c = conn.execute("SELECT * FROM users WHERE username GLOB ?", (username,))
    row = c.fetchone()
    if not row:
        return None
    return { "id": row[0], "username": row[1], "hash": row[2], "salt": row[3] }


# This method is called to get a User object based on a request,
# for example, if using an api key or authentication token rather
# than getting the username the standard way (from the session cookie)
@login_manager.request_loader
def request_loader(request):
    # Even though this HTTP header is primarily used for *authentication*
    # rather than *authorization*, it's still called "Authorization".
    auth = request.headers.get('Authorization')

    # If there is no Authorization header, do nothing, and the login
    # manager will deal with it (i.e., by redirecting to a login page)
    if not auth:
        return

    (auth_scheme, auth_params) = auth.split(maxsplit=1)
    auth_scheme = auth_scheme.casefold()
    print("Authorization scheme: ", auth_scheme)
    if auth_scheme == 'basic':  # Basic auth has username:password in base64
        (uid,passwd) = b64decode(auth_params.encode(errors='ignore')).decode(errors='ignore').split(':', maxsplit=1)
        print(f'Basic auth: {uid}:{passwd}')
        user = get_user(uid)
        if user and login.check_password(passwd, user.get("salt"), user.get("hash")):
            return user_loader(uid)
    elif auth_scheme == 'bearer': # Bearer auth contains an access token;
        # an 'access token' is a unique string that both identifies
        # and authenticates a user, so no username is provided (unless
        # you encode it in the token – see JWT (JSON Web Token), which
        # encodes credentials and (possibly) authorization info)
        print(f'Bearer auth: {auth_params}')
        for uid in users:
            if users[uid].get('token') == auth_params:
                return user_loader(uid)


    # For other authentication schemes, see
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication

    # If we failed to find a valid Authorized header or valid credentials, fail
    # with "401 Unauthorized" and a list of valid authentication schemes
    # (The presence of the Authorized header probably means we're talking to
    # a program and not a user in a browser, so we should send a proper
    # error message rather than redirect to the login page.)
    # (If an authenticated user doesn't have authorization to view a page,
    # Flask will send a "403 Forbidden" response, so think of
    # "Unauthorized" as "Unauthenticated" and "Forbidden" as "Unauthorized")
    abort(HTTPStatus.UNAUTHORIZED, www_authenticate = WWWAuthenticate('Basic realm=inf226, Bearer'))

@app.route('/favicon.ico')
def favicon_ico():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/favicon.png')
def favicon_png():
    return send_from_directory(app.root_path, 'favicon.png', mimetype='image/png')

@app.get('/useridinfo')
@login_required
def useridinfo():
    id_str = request.args.get("id")
    try:
        user_id = int(id_str)
    except:
        user_id = 0
    user = User(user_id)
    return dumps({"id": user.id, "username": user.username})


@app.route('/')
@app.route('/index.html')
@login_required
def index_html():
    return send_from_directory(app.root_path,
                        'index.html', mimetype='text/html')

@app.get('/coffee/')
def nocoffee():
    abort(418)

@app.route('/coffee/', methods=['POST','PUT'])
def gotcoffee():
    return "Thanks!"

@app.get('/highlight.css')
def highlightStyle():
    resp = make_response(cssData)
    resp.content_type = 'text/css'
    return resp

try:
    conn = apsw.Connection('./tiny.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL);''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id integer PRIMARY KEY,
        sender TEXT NOT NULL,
        message TEXT NOT NULL);''')
    c.execute('''CREATE TABLE IF NOT EXISTS announcements (
        id integer PRIMARY KEY,
        author TEXT NOT NULL,
        text TEXT NOT NULL);''')
except Error as e:
    print(e)
    sys.exit(1)

import login
import register
import messaging
