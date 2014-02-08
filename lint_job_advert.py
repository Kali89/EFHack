import requests
import json
payload = {'spec':"Your job spec goes here"}
headers = {'User-Agent':'MyApp/1.0', 'Content-Type':'application/json'}
r = requests.post("http://joblint.org/ws", headers=headers, data=json.dumps(payload))
print json.dumps(payload)
print r.text
