import os


def configure(app):
    app.secret_key = os.getenv('FLASK_SECRET_KEY') or 'reallystrongsecretkey'

    app.config['PG_USER'] = os.getenv('POSTGRES_USER')
    app.config['PG_PASSWORD'] = os.getenv('POSTGRES_PASSWORD')
    app.config['PG_HOST'] = os.getenv('PG_HOST')
    app.config['DATABASE'] = os.getenv('POSTGRES_DB')

    app.config['REDIS_HOST'] = os.getenv('REDIS_HOST') or '127.0.0.1'
    app.config['REDIS_PORT'] = os.getenv('REDIS_PORT') or 6379
    app.config['REDIS_DB'] = 0

    app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY') or ''
    app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY') or ''
    app.testing = os.getenv('TESTING').upper() == 'TRUE'

    app.config['ADMIN_LOGIN'] = os.getenv('ADMIN_LOGIN') or 'admin'
    app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD') or 'reallYS3cretPassw0rdN0L3ak'
    app.config['FLAG'] = os.getenv('FLAG') or 'flag{flag}'
    app.config.update(
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_HTTPONLY=True,
    )

    return app