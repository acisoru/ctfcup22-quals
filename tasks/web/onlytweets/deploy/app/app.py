import base64
import functools
import json
import secrets
import uuid
import redis

from flask import Flask, g, session, render_template, redirect, request, flash, abort, jsonify
from flask_wtf.csrf import CSRFProtect
from pony import orm

from config import configure
from db import bind_db
from model import User, Tweet
from forms import ReportForm

csrf = CSRFProtect()

app = Flask(__name__)

app = configure(app)

csrf.init_app(app)

bind_db(app)


def get_redis():
    redis_cli = getattr(g, '_redis', None)
    if redis_cli is None:
        redis_cli = g._redis = redis.Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'],
                                           db=app.config['REDIS_DB'])
    return redis_cli


def login_required(f):
    @functools.wraps(f)
    def inner_handle(*args, **kwargs):
        if 'user_id' in session:
            return f(*args, **kwargs)
        abort(403)

    return inner_handle


@app.before_request
def load_user():
    g.user = None
    if "user_id" in session:
        g.user = User.select(id=session.get('user_id')).first()
    return


@app.before_request
def fill_nonce():
    g.nonce = base64.b64encode(secrets.token_bytes(20)).decode()[:-1]


@app.route('/')
def index():
    user = session.get('user_id')
    if user is None:
        return render_template('index.html')

    feed_tweets = Tweet.select(lambda t: t.public).order_by(lambda t: orm.desc(t.id))[:50]
    shared_tweets = list(g.user.shared_tweets)
    return render_template('feed.html', feed_tweets=feed_tweets, shared_tweets=shared_tweets)


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if username == '' or password == '':
        flash('Empty login or password', category='error')
        return render_template('register.html'), 412

    try:
        with orm.db_session:
            User(login=username, password=password)
    except orm.core.TransactionIntegrityError:
        flash('User already exists.')
        return render_template('register.html'), 412
    except Exception as e:
        if 'duplicate key value' in str(e):
            flash('User already exists.')
            return render_template('register.html'), 412
        raise e

    return redirect('/login')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template('login.html')

    username = request.values.get('username')
    password = request.values.get('password')

    with orm.db_session:
        user = User.select(lambda u: u.login == username and u.password == password).first()
        if user:
            session['user_id'] = user.id
            return redirect('/')

    flash("No such user")
    return render_template('login.html')


@app.route('/create_tweet', methods=["GET", "POST"])
@login_required
def tweet():
    if request.method == "GET":
        return render_template('tweet_create.html')

    content = request.values.get('content')
    is_public = request.values.get('public') == 'true'

    if content == "":
        flash('Please specify tweet text.')
        return render_template('tweet_create.html')

    with orm.db_session:
        Tweet(text=content, public=is_public, author=g.user)

    return redirect('/')


@app.route('/profile', methods=["POST", "GET"])
@login_required
def profile():
    if request.method == 'GET':
        return render_template('profile.html', tweets=list(g.user.tweets))

    userpic = request.values.get('userpic')
    with orm.db_session:
        g.user.user_pic = userpic
    return redirect('/profile')


@app.route('/share', methods=["POST", "GET"])
@login_required
def share():
    if request.method == "GET":
        return render_template('share.html', user=session.get('username'))

    tweet_id = request.values.get('tweet_id')
    to_user = request.values.get('to_user')

    if tweet_id not in set([str(t.id) for t in g.user.tweets]):
        abort(403)
        return

    to_user = User.select(lambda u: u.login == to_user).first()
    if to_user is None:
        return 'Failed to find user', 412

    tweet = Tweet[int(tweet_id)]
    tweet.shared_to.add(to_user)

    return redirect('/profile')


@app.route('/user/<username>')
def user_tweets(username):
    print(username)
    user = User.select(lambda u: u.login == username).first()
    if user is None:
        abort(404)

    return render_template('user_page.html', user=user)


@app.route('/tweet/<tweet_id>')
def tweet_page(tweet_id):
    return render_template('tweet_page.html', tweet_id=tweet_id)


@app.route('/api/tweet/<tweet_id>')
def tweet_get(tweet_id):
    try:
        tweet = Tweet[tweet_id]
        if tweet.public or g.user and (tweet in g.user.tweets or tweet in g.user.shared_tweets):
            return jsonify({'content': tweet.text, 'id': tweet.id,
                            'author': {'name': tweet.author.login, 'pic': tweet.author.user_pic}})
        abort(403)
    except orm.core.ObjectNotFound:
        abort(404)


@app.route('/report', methods=["POST", "GET"])
@login_required
def report():
    report_form = ReportForm()
    if report_form.validate_on_submit():
        uid = str(uuid.uuid4())
        redis_cli = get_redis()
        redis_cli.rpush('report-queue', json.dumps({'url': report_form.report_url.data, 'uid': uid}))
        redis_cli.set('reports:' + uid, 'false')
        return redirect('/reports/{}'.format(uid))

    return render_template('report.html', form=report_form)


@app.route('/reports/<report_id>')
def report_page(report_id):
    redis_cli = get_redis()
    status = redis_cli.get('reports:' + report_id)
    if status is None:
        abort(404)

    queue_len = redis_cli.llen('report-queue')
    return render_template('report_status.html', status=status.decode(), queue_len=queue_len, report_id=report_id)


@app.route('/logout', methods=['POST', 'GET'])
def logout_page():
    if request.method == 'POST':
        session.clear()
        return redirect('/')

    return render_template('logout.html')


@app.after_request
def set_headers(response):
    response.headers[
        'Content-Security-Policy'] = '''default-src 'self'; img-src * ; script-src 'nonce-{nonce}' 'unsafe-eval' www.google.com; style-src 'unsafe-inline' cdn.jsdelivr.net; frame-src www.google.com '''.format(
        nonce=g.nonce)
    return response
