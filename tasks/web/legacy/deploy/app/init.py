from app import get_db, app, Secret, password_hash

if __name__ == '__main__':
    with app.app_context():
        db = get_db()
        db.save_user('admin', password_hash(app.config['ADMIN_PASSWORD']))
        if not db.get_user_secrets('admin'):
            db.save_secret('admin', Secret(name='flag', content=app.config['FLAG'], author='admin'))

