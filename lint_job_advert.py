import requests
import json


def lint_job_description(job_description):
    payload = {'spec':job_description}
    headers = {'User-Agent':'MyApp/1.0', 'Content-Type':'application/json'}
    r = requests.post("http://joblint.org/ws", headers=headers, data=json.dumps(payload))
    return json.loads(r.text)

lint_job_description("Fucking Beer, Tits and XBox Brah!")
