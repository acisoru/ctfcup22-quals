from pony import orm
from db import db


class User(db.Entity):
    # id = orm.PrimaryKey(int, auto=True)
    login = orm.Required(str, unique=True)
    password = orm.Required(str)
    user_pic = orm.Optional(str)
    tweets = orm.Set('Tweet', reverse='author')
    shared_tweets = orm.Set('Tweet', reverse='shared_to')


class Tweet(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    text = orm.Required(str)
    public = orm.Required(bool)
    author = orm.Required(User)
    shared_to = orm.Set(User)
