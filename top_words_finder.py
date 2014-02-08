#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import argparse
import re
from argparse import ArgumentParser
import os.path
import manual_tfidf

## Get all the jobs out of the database
with open('user_password.txt') as f:
    username, password = f.readline().strip().split(':')
    con = mdb.connect('10.100.95.207', username, password, 'test');
    with con:
        cur = con.cursor()
        all_descriptions_sql = "SELECT search_id, job_title, job_description from test.job_results LIMIT 10"
        cur.execute(all_descriptions_sql)
        id_title_description = [[entry[0], entry[1], entry[2]] for entry in cur.fetchall()]

all_descriptions = [entry[2].strip().decode('utf-8', 'ignore').lower().replace(',', ' ').strip() for entry in id_title_description if len(entry[2].strip().decode('utf-8', 'ignore')) > 25]
new_descriptions = []
better_descriptions = [thing.split(' ') for thing in all_descriptions]
for index in range(len(better_descriptions)):
    new_document = ' '.join([word.strip().replace(',',' ').replace('\t', ' ').strip() for word in better_descriptions[index] if len(word.strip().replace(',',' ').replace('\t', ' ').strip()) > 1])
    new_descriptions.append(new_document)

def get_docs_by_job_id(job_ids):
    with open('user_password.txt') as f:
        username, password = f.readline().strip().split(':')
        con = mdb.connect('10.100.95.207', username, password, 'test');
        with con:
            cur = con.cursor()
            all_descriptions_sql = "SELECT search_id, job_title, job_description from test.job_results where search_id in " + array_to_sql(job_ids) + " LIMIT 10"
            cur.execute(all_descriptions_sql)
            id_title_description = [[entry[0], entry[1], entry[2]] for entry in cur.fetchall()]

    all_descriptions = [entry[2].strip().decode('utf-8', 'ignore').lower().replace(',', ' ').strip() for entry in id_title_description if len(entry[2].strip().decode('utf-8', 'ignore')) > 25]
    new_descriptions = []
    better_descriptions = [thing.split(' ') for thing in all_descriptions]
    for index in range(len(better_descriptions)):
        new_document = ' '.join([word.strip().replace(',',' ').replace('\t', ' ').strip() for word in better_descriptions[index] if len(word.strip().replace(',',' ').replace('\t', ' ').strip()) > 1])
        new_descriptions.append(new_document)

    return new_descriptions

def array_to_sql(arr):
    return '(' + ', '.join(str(x) for x in arr) + ')'

nd_2 = get_docs_by_job_id([1,2,3])
print nd_2
manual_tfidf.new_run_tfidf(new_descriptions)

