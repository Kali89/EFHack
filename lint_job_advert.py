import requests
import json


def lint_job_description(job_description):
    payload = {'spec':job_description}
    headers = {'User-Agent':'MyApp/1.0', 'Content-Type':'application/json'}
    r = requests.post("http://joblint.org/ws", headers=headers, data=json.dumps(payload))
    return json.loads(r.text)

def is_job_description_good(job_description):
    job_dict = lint_job_description(job_description)
    return job_dict['warnings']

print is_job_description_good("Beer and XBox Brah!")
print "%%%%%%%"
print is_job_description_good("This is a job")
