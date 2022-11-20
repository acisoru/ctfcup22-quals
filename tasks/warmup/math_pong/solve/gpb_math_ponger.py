#!/usr/bin/env python3 
import requests, random, string, re
url = "http://127.0.0.1:8181/api/"
with requests.Session() as s:
    login = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    s.headers.update({"Content-Type":"application/json"})
    r = s.get(url)
    r = s.post(url + "signup", json={"login":login, "password":password})
    r = s.post(url + "signin", json={"login":login, "password":password})
    for k,v in r.cookies.get_dict().items():
        s.cookies.set(k,v)
    r = s.get(url + "shop")
    price = int(re.search(r"flag price is ([\d]*) coins", r.json()["result"])[1])
    print(price)
    for i in range(price):
        r = s.get(url + "task")
        task_result = eval(r.json()["result"])
        r = s.post(url + "task", data=str(task_result))
    r = s.post(url + "shop")
    print(r.text)
        
