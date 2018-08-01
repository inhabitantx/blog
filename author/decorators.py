from functools import wraps
from flask import redirect, session, request, url_for, abort


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') == None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def author_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username'):
            if session.get('is_author') == None:
                abort(403)
        else:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username'):
            if session.get('is_admin') == None:
                abort(403)
        else:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
