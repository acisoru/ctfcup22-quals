import redis
import hashlib
import requests
import logging
from flask import Flask, g, render_template, request, flash, redirect, make_response

from config import configure
from db import DB, Secret

app = Flask(__name__)
app = configure(app)


def get_redis():
    red = getattr(g, '_redis', None)
    if red is None:
        red = g._redis = redis.Redis(app.config['REDIS_HOST'], app.config['REDIS_PORT'], db=0)
    return red


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = DB(get_redis())
    return db


def get_session_user():
    session_cookie = request.cookies.get('lsession')
    if session_cookie is None:
        return None

    redis_cli = get_redis()
    user = redis_cli.get('sessions|' + session_cookie)
    if user is not None:
        return user.decode()

    try:
        resp = requests.get('http://{}/cgi-bin/sessvalid.pl'.format(app.config['AUTH_HOST']),
                            headers={
                                'SecretKey': app.config['AUTH_KEY']
                            }, cookies={
                'lsession': session_cookie
            })
        resp_j = resp.json()
        status = resp_j.get('status')
        if status != 'ok':
            logging.error('Session generation failed: {}'.format(status))
            return None

        user = resp_j.get('user')
        redis_cli.set('sessions|' + session_cookie, user, ex=60)
        return user

    except Exception as e:
        logging.error('Session validation failed: {}'.format(e))
        return None


def generate_session(user):
    try:
        resp = requests.get('http://{}/cgi-bin/sessgen.pl'.format(app.config['AUTH_HOST']), params={'user': user},
                            headers={
                                'SecretKey': app.config['AUTH_KEY']
                            })
        json_r = resp.json()
        status = json_r.get('status', '')
        if status == 'ok':
            return resp.cookies.get('lsession')
        else:
            logging.error('Session generation failed: {}'.format(status))
            return None
    except Exception as e:
        logging.error('Session generation failed: {}'.format(e))
        return None


def password_hash(pwd: str):
    return hashlib.sha1(pwd.encode()).hexdigest()


@app.before_request
def load_user():
    g.user = get_session_user()
    return


@app.get('/')
def index_page():
    if g.user is None:
        return render_template('index.html')

    db = get_db()
    secrets = db.get_user_secrets(g.user)
    return render_template('home.html', secrets=secrets)


@app.post('/create')
def create_handle():
    if g.user is None:
        return redirect('/')

    name = request.values.get('name')
    content = request.values.get('content')

    db = get_db()
    db.save_secret(user_id=g.user, secret=Secret(name=name, content=content, author=g.user))
    return redirect('/')


@app.get('/register')
def register_page():
    return render_template('register.html')


@app.post('/register')
def register_handle():
    db = get_db()

    username = request.values.get('username', '')
    password = request.values.get('password', '')
    if username == '' or password == '':
        flash('Empty login or password', category='error')
        return render_template('register.html'), 418

    if db.user_exists(username):
        flash('User already exists', category='error')
        return render_template('register.html'), 418

    db.save_user(username, password_hash(password))

    return redirect('/login')


@app.get('/login')
def login_page():
    return render_template('login.html')


@app.post('/login')
def login_handle():
    username = request.values.get('username', '')
    password = request.values.get('password', '')

    db = get_db()

    if db.validate_user_credentials(username, password_hash(password)):
        session_val = generate_session(username)
        if session_val is None:
            flash('Failed to generate session')
            return render_template('login.html')

        resp = make_response(redirect('/'))
        resp.set_cookie('lsession', session_val)
        return resp

    flash('No user found', category='error')
    return render_template('login.html')


@app.get('/logout')
def logout_page():
    resp = make_response(redirect('/'))
    resp.set_cookie('lsession', expires=0)
    return resp
