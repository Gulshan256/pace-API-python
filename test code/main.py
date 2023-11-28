import http.client
import json

clintid ="PACE-CSG981"
conn = http.client.HTTPSConnection("pacetrader.pacefin.in")
payload = ''
headers = {
  'P-DeviceType': 'WEB',
  'Content-Type': 'application/json',
  'accept': 'application/json'
}
conn.request("GET", "/oauth2/auth?scope=orders%20holdings&state=3unqcjh2DN1o&redirect-uri=http://127.0.0.1/&response_type=code&client_id={clintid}", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))