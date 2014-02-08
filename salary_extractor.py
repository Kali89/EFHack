#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
import nltk
import MySQLdb as mdb
import sys
import argparse
import re
from argparse import ArgumentParser
import os.path

parser = ArgumentParser(description='Get a search id')
parser.add_argument('-i', dest="search_id", required=True, metavar='search_id', help="salary for given search id", type=int)
args = parser.parse_args()

## Get all the jobs out of the database
with open('user_password.txt') as f:
    username, password = f.readline().strip().split(':')
con = mdb.connect('localhost', username, password, 'test');
with con:
    cur = con.cursor()
    all_descriptions_sql = "SELECT job_title, job_description from test.job_results where search_id = " + str(args.search_id)
    cur.execute(all_descriptions_sql)
    title, description = cur.fetchall()[0]

small_salary_regex = re.compile('\d{2,3}(?=k|K)')
salary_regex = re.compile('\d{2}0{1,4}')
further_salary_regex = re.compile('\d{2,3},\d{1,4}')
pound_salary_regex = re.compile('\£\d+(?=k|K|thousand)')
further_pound_salary_regex = re.compile('£\w+(?=k|K|thousand|p//day|per|p//week|p//month|p//annum)')

if re.findall(further_salary_regex, title) or re.findall(further_salary_regex, description):
    if re.findall(further_salary_regex, title):
        print str(re.findall(further_salary_regex, title)[0])
    else:
        print str(re.findall(further_salary_regex, description)[0])
elif re.findall(pound_salary_regex, title) or re.findall(pound_salary_regex, description):
    if re.findall(pound_salary_regex, title):
        print str(re.findall(pound_salary_regex, title)[0])
    else:
        print str(re.findall(pound_salary_regex, description)[0])
elif re.findall(further_pound_salary_regex, title) or re.findall(further_pound_salary_regex, description):
    if re.findall(further_pound_salary_regex, title): 
        print str(re.findall(further_pound_salary_regex, title)[0])
    else:
        print str(re.findall(further_pound_salary_regex, description)[0])
elif re.findall(salary_regex, title) or re.findall(salary_regex, description):
    if re.findall(salary_regex, title):
        print str(re.findall(salary_regex, title)[0])
    else:
        print str(re.findall(salary_regex, description)[0])
elif re.findall(small_salary_regex, title) or re.findall(small_salary_regex, description):
    if re.findall(small_salary_regex, title):
        print str(re.findall(small_salary_regex, title)[0])
    else:
        print str(re.findall(small_salary_regex, description)[0])
else:
    print "Can't find a salary"


