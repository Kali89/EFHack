#!/usr/bin/python

import argparse
from argparse import ArgumentParser
from job_search import job_search_runner, open_and_parse_job_websites
import Queue
import threading

concurrent = 4

parser = ArgumentParser(description='Take a job search file and perform the seaches')
parser.add_argument('-i', dest="input_file", required=True, metavar='FILE', help="job search file path")
args = parser.parse_args()

def run_query_set():
    while True:
        line = q.get()
        job, location = line.strip().split(':')
        indeed_scraper = job_search_runner(job, location)
        job_site_scraper = open_and_parse_job_websites()
        for key, value in indeed_scraper.job_dictionary.items():
            job_site_scraper.open_website(key, job, location, value)
        q.task_done()

job_dictionary = {}
q = Queue.Queue()
with open(args.input_file, 'rb') as f:
    for line in f.readlines():
        q.put(line.strip())
#        job, location = line.strip().split(':')
#        job_dictionary[job] = location

print "Queue filled"

for item in range(concurrent):
    print "Thread %s started" % str(int(item) + 1)
    t = threading.Thread(target=run_query_set)
    t.daemon = True
    t.start()

print "All threads started"
q.join()
print "All items searched for"
#for job in job_dictionary.keys():
#    q.put(job, job_dictionary[job])
#    indeed_scraper = job_search_runner(job, job_dictionary[job])
#    job_site_scraper = open_and_parse_job_websites()
#    for key, value in indeed_scraper.job_dictionary.items():
#        job_site_scraper.open_website(key, args.job_search_term, args.location_search_term, value)
   

