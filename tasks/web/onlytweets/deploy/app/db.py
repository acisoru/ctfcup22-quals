import flask
from pony.orm import Database
from pony.flask import Pony

db = Database()


def bind_db(app: flask.Flask):
    db.bind('postgres',
            user=app.config['PG_USER'],
            password=app.config['PG_PASSWORD'],
            host=app.config['PG_HOST'],
            database=app.config['DATABASE'])
    db.generate_mapping(create_tables=True)
    Pony(app)
