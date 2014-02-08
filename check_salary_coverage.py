#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import argparse
import re
from argparse import ArgumentParser
import os.path

## Get all the jobs out of the database
with open('user_password.txt') as f:
    username, password = f.readline().strip().split(':')
    con = mdb.connect('10.100.95.207', username, password, 'test');
    with con:
        cur = con.cursor()
        all_descriptions_sql = "SELECT job_title, job_description from test.job_results"
        cur.execute(all_descriptions_sql)
        title_description = [[entry[0], entry[1]] for entry in cur.fetchall()]

small_salary_regex = re.compile('\d{2,3}(?=k|K)')
salary_regex = re.compile('\d{2}0{1,4}')
further_salary_regex = re.compile('\d{2,3},\d{1,4}')
pound_salary_regex = re.compile('\£\d+(?=k|K|thousand)')
further_pound_salary_regex = re.compile('£\w+(?=k|K|thousand|p//day|per|p//week|p//month|p//annum)')

def extract_salary(title_description_list_entry):
    title, description = title_description_list_entry
    if re.findall(further_salary_regex, title) or re.findall(further_salary_regex, description):
        if re.findall(further_salary_regex, title):
            return re.findall(further_salary_regex, title)[0]
        else:
            return re.findall(further_salary_regex, description)[0]
    elif re.findall(pound_salary_regex, title) or re.findall(pound_salary_regex, description):
        if re.findall(pound_salary_regex, title):
            return re.findall(pound_salary_regex, title)[0]
        else:
            return re.findall(pound_salary_regex, description)[0]
    elif re.findall(further_pound_salary_regex, title) or re.findall(further_pound_salary_regex, description):
        if re.findall(further_pound_salary_regex, title):
            return re.findall(further_pound_salary_regex, title)[0]
        else:
            return re.findall(further_pound_salary_regex, description)[0]
    elif re.findall(salary_regex, title) or re.findall(salary_regex, description):
        if re.findall(salary_regex, title):
            return re.findall(salary_regex, title)[0]
        else:
            return re.findall(salary_regex, description)[0]
    elif re.findall(small_salary_regex, title) or re.findall(small_salary_regex, description):
        if re.findall(small_salary_regex, title):
            return re.findall(small_salary_regex, title)[0]
        else:
            return re.findall(small_salary_regex, description)[0]
    else:
        pass

coverage_test = dict((i, extract_salary(title_description_list_entry)) for i, title_description_list_entry in enumerate(title_description))
total_salaries_found = len([coverage_test[i] for i in coverage_test.keys() if coverage_test[i]])
total_entries_in_database = len(coverage_test)
print "Found %s salaries out of %s entries" % (str(total_salaries_found), str(total_entries_in_database))
