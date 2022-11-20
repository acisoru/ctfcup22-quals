import os


def configure(app):
    app.secret_key = os.getenv('FLASK_SECRET_KEY') or 'reallystrongsecretkey'
    app.config['REDIS_HOST'] = os.getenv('REDIS_HOST') or '127.0.0.1'
    app.config['REDIS_PORT'] = int(os.getenv('REDIS_PORT') or 6379)
    app.config['REDIS_URL'] = 'redis://{}:{}'.format(app.config['REDIS_HOST'], app.config['REDIS_PORT'])

    app.config['AUTH_HOST'] = os.getenv('AUTH_HOST') or 'localhost:8888'
    app.config['AUTH_KEY'] = os.getenv('AUTH_KEY') or 'authKey'

    app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD') or '12345'
    app.config['FLAG'] = os.getenv('FLAG') or 'CUP{example}'
    return app