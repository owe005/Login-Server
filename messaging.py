from app import app, tls, conn, user_loader
from flask import request
import flask_login
from flask_login import login_required
from json import dumps
from apsw import Error
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import HtmlFormatter
from pygments.filters import NameHighlightFilter, KeywordCaseFilter
from pygments import token
from markupsafe import escape
from datetime import datetime

from login import get_current_user


### Moved from app.py
def pygmentize(text):
    if not hasattr(tls, 'formatter'):
        tls.formatter = HtmlFormatter(nowrap = True)
    if not hasattr(tls, 'lexer'):
        tls.lexer = SqlLexer()
        tls.lexer.add_filter(NameHighlightFilter(names=['GLOB'], tokentype=token.Keyword))
        tls.lexer.add_filter(NameHighlightFilter(names=['text'], tokentype=token.Name))
        tls.lexer.add_filter(KeywordCaseFilter(case='upper'))
    return f'<span class="highlight">{highlight(text, tls.lexer, tls.formatter)}</span>'
###

@app.get('/search')
@login_required

def search():
    query = request.args.get('q') or request.form.get('q') or '*'
    stmt = f"SELECT * FROM messages WHERE message GLOB '{query}'"
    result = f"Query: {pygmentize(stmt)}\n"

    try:
        c = conn.execute("SELECT * FROM messages WHERE message GLOB ?", (query,))
        rows = c.fetchall()
        result = result + 'Result:\n'

        for row in rows:
            result = f'{result}    {escape(dumps(row))}\n'
        c.close()

        return result

    except Error as e:
        return f'{result}ERROR: {e}', 500


@app.route('/send', methods=['POST','GET'])
@login_required

def send():
    try:
        user = get_current_user()
        sender = user.username
        message = request.args.get('message') or request.args.get('message')

        stmt = f"INSERT INTO messages (sender, message) values ('{sender}', '{message}');"
        result = f"Query: {pygmentize(stmt)}\n"
        conn.execute("INSERT INTO messages (sender, message) values (?, ?);", (sender, message))

        ### Time shenanigans ###
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        output = '>' + current_time + ' ' + sender + ': ' + message
        return output

    except Error as e:
        return f'{result}ERROR: {e}'
