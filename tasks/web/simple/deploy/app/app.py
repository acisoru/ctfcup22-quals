import base64
import json
import jwt
import hashlib
import hmac
import os

from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__)

with open('/keys/privkey.pem') as private_key_file:
    private_key = private_key_file.read()

with open('/keys/cert.pem') as public_key_file:
    public_key = public_key_file.read()

flag = os.environ.get("FLAG", "CUP")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']

    data = {"login": login, 'is_admin': False}
    encoded = jwt.encode(data, private_key, algorithm="RS256")

    response = make_response(redirect('/profile'))
    response.set_cookie('token', encoded)
    return response

@app.route('/profile')
def profile():
    token = request.cookies.get('token')
    key = public_key
    try:
        header = jwt.get_unverified_header(token)
        print(header)
        alg = header.get('alg', '')
        if alg and alg.lower() == 'none':
            return "That would be too easy"

        if alg == 'HS256':
            key = key.replace('-----BEGIN PUBLIC KEY-----', '').replace('-----END PUBLIC KEY-----', '').strip('\n')

        print("Part 1")
        print(key)
        decoded = jwt.decode(token, key, algorithms=["RS256", "HS256"])

    except jwt.exceptions.InvalidSignatureError as e:
        print(e)
        print('Plan B')
        # Библиотека jwt не позволяет использовать публичный ключ для алгоритма RS256.
        # Для тех команд, которые все-таки как-то подпишут токен таким ключом, делаю запасной вариант
        parts = token.split('.')

        user_sign = parts[2].encode()
        print(public_key.encode())
        print(parts[0])
        print(parts[1])
        our_sign = hmac.new(public_key.encode(), (parts[0] + '.' + parts[1]).encode(), hashlib.sha256).digest()
        our_sign = base64.b64encode(our_sign).rstrip(b"=")

        compare = hmac.compare_digest(our_sign, user_sign)
        if not compare:
            print(f"user_sign {user_sign}")
            print(f"our_sign {our_sign}")

            response = make_response(redirect('/'))
            response.set_cookie('token', '')
            return response

        decoded = json.loads(base64.b64decode(parts[1] + '=' * (-len(parts[1]) % 4)))
    except Exception as e:
        print("Global exception")
        print(e)
        response = make_response(redirect('/'))
        response.set_cookie('token', '')
        return response

    print(decoded)
    return render_template('profile.html', list=decoded, flag=flag)


if __name__ == '__main__':
    app.run()
