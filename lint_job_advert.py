import requests
import json


def lint_job_description(job_description):
    payload = {'spec':job_description}
    headers = {'User-Agent':'MyApp/1.0', 'Content-Type':'application/json'}
    r = requests.post("http://joblint.org/ws", headers=headers, data=json.dumps(payload))
    return json.loads(r.text)

def is_job_description_good(job_description):
    job_dict = lint_job_description(job_description)
    for failure, count in job_dict['failPoints'].items():
        if count > 0:
            return False
    for warning in job_dict['warnings']:
        pass
        #print warning.items()
    return True

"""
print is_job_description_good("Beer and XBox Brah!")
print "%%%%%%%"
print is_job_description_good("This is a job")
"""
