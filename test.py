


import http.client
import webbrowser
import json

conn = http.client.HTTPSConnection("pacetrader.pacefin.in")
payload = ''
headers = {
  'P-DeviceType': 'WEB',
  'Content-Type': 'application/json',
  'accept': 'application/json'
}

conn.request("GET", "/oauth2/auth?scope=orders%20holdings&state=3unqcjh2DN1o&redirect-uri=pacetrader.pacefin.in/&response_type=code&client_id={clintId}", payload, headers)



res = conn.getresponse()
print(res.status, res.reason)
data = res.read().decode("utf-8").split('"')[1]
print(data)
webbrowser.open(data)


# # error after this
# http://127.0.0.1/?error=request_forbidden&error_description=The+request+is+not+allowed&error_hint=You+are+not+allowed+to+perform+this+action.&state=3unqcjh2DN1o

