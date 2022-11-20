from flask import Flask

from config import configure
from db import bind_db

from pony import orm

from model import User, Tweet

app = Flask(__name__)

app = configure(app)

bind_db(app)

with orm.db_session:
    user = User.select(lambda u: u.login == app.config['ADMIN_LOGIN']).first()
    print(user)
    if user is None:
        user = User(login=app.config['ADMIN_LOGIN'], password=app.config['ADMIN_PASSWORD'])

    if len(user.tweets) == 0:
        Tweet(text=app.config['FLAG'], public=False, author=user)
