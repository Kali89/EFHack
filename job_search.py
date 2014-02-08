#!/usr/bin/python

import mechanize
from bs4 import BeautifulSoup
import re
import time
import MySQLdb as mdb
import argparse
from argparse import ArgumentParser

def get_arguments():
    parser = ArgumentParser(description='Take a job search and a location term')
    parser.add_argument('-j', dest="job_search_term", required=True, metavar='STR', help="job search term", type=str)
    parser.add_argument('-l', dest="location_search_term", required=True, metavar='STR', help="location search term", type=str)
#    args = parser.parse_args()
    return parser.parse_args()

class Indeed_search_handler(object):
    """
    This will find the Indeed job form, post a job search and get back the results
    """
    def __init__(self):
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.browser.set_handle_refresh(False)
        self.browser.set_handle_equiv(False)
        self.browser.addheaders = [('User-agent', 'Chrome'), ('Accept', '*/*')]
        self.response_text = ""
        self.job_search_regex = re.compile('jk\=')
        self.next_page_regex = re.compile('start\=')
        self.job_dictionary = {}
        self.parsed_site = None
        self.last_page_link = ""
        self.number_of_results = 0
        self.current_page_text = ""
        self.form_response_text = None
        self.link_dictionary = {}
        self.new_link_dictionary = {}


    def open_website(self, root_url="http://www.indeed.co.uk/", attempts = 3):
        """
        Opens up a webpage and tries to get the text on it
        """
### Marked for tidying
        self.current_page_text = ""
        attempt_number = 0
        while attempt_number < attempts and not self.current_page_text:
            try:
                self.current_page_text = str(self.browser.open(root_url).read())
            except:
                attempt_number += 1
                time.sleep(2)

    def get_all_form(self):
        """
        Get all the forms on the current page
        """
        form_list = [form for form in self.browser.forms()]
        ## The job entry form is the first one on the homepage
        self.browser.form = form_list[0]
        self.browser.select_form("jobsearch")
        ## Need to make sure we can enter infomation in the form
        self.browser.set_all_readonly(False)

    def enter_form_values(self, job_title, location):
        """
        Input job title and location terms into the search fields of the homepage form
        """
        control_list = [control_name for control_name in self.browser.form.controls]
        ## The first and second fields in the form
        job_title_entry = self.browser.form.find_control(control_list[0].name)
        location_title_entry = self.browser.form.find_control(control_list[1].name)
        #job_title_entry = self.browser.form.find_control("q")
        #location_title_entry = self.browser.form.find_control("l")
        ## Modify the values
        job_title_entry.value = job_title
        location_title_entry.value = location

    def submit_form(self):
        """
        Submit the current form and get the text from the next page
        """
        self.current_page_text = self.browser.submit()


    def get_job_links_from_page(self):
        """
        Given some text on the current page - run through the links and create a dictionary of job link to job title
        """
        ## Marked for tidying
        if self.current_page_text:
            self.parsed_site = BeautifulSoup(self.current_page_text)
            holding_dictionary = dict((link.get('href'), link.get('title')) for link in self.parsed_site.find_all('a') if re.findall(self.job_search_regex, link.get('href')) and link.get('title'))
            self.job_dictionary.update(holding_dictionary)

    def get_next_page_of_results(self):
        """
        Find the next page of results for search terms with multiple results and add to the new link dictionary
        """
        holding_dictionary = dict(("http://www.indeed.co.uk" + str(link.get('href')), False) for link in self.parsed_site.find_all('a') if re.findall(self.next_page_regex, link.get('href')))
        self.new_link_dictionary.update(holding_dictionary)

    def run_iteration(self):
        """
        Descend to a page depth of 20
        """
        ## Marked for tidying
        i = 0
        while i < 20:
            self.link_dictionary = dict(self.new_link_dictionary.items() + self.link_dictionary.items())
            self.new_link_dictionary = {}
            i += 1
            for link, status in self.link_dictionary.items():
                if not self.link_dictionary[link]:
                    self.open_website(link)
                    self.get_job_links_from_page()
                    self.link_dictionary[link] = True
                    self.get_next_page_of_results()


    def return_self(self):
        return self

def job_search_runner(job_search_term, location_term):
    ## Marked for tidying
    mySite = Indeed_search_handler()
    mySite.open_website()
    mySite.get_all_form()
    mySite.enter_form_values(job_search_term, location_term)
    mySite.submit_form()
    mySite.get_job_links_from_page()
    mySite.get_next_page_of_results()
    mySite.run_iteration()
    y = mySite.return_self()
    return y

class open_and_parse_job_websites(object):
    def __init__(self):
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.browser.set_handle_refresh(False)
        self.browser.addheaders = [('User-agent', 'Chrome'), ('Accept', '*/*')]
        self.browser.set_handle_equiv(False)
        self.website_text = ""

    def open_website(self, url, job_search_term, location_search_term, job_title, root_url="http://www.indeed.co.uk"):
        ## Marked for tidying
        full_url = root_url + url
        soup = ""
        attempt_number = 0
        attempts = 3
        while attempt_number < attempts and not soup and not soup:
            try:
                soup = BeautifulSoup(self.browser.open(full_url).read().decode('utf-8', 'ignore').strip())
            except:
                print ""
            attempt_number += 1
            time.sleep(2)

        if not soup:
            website_text = "Not found"
        else:
            website_text = ""
            for row in soup.find_all('p'):
                text = ' '.join(row.findAll(text=True))
                website_text = website_text + "\n" + text

        self.singular_insert_into_database(job_search_term, location_search_term, job_title, website_text)

    def singular_insert_into_database(self, job_search_term, location_search_term, key, website_text):
        ## Marked for tidying
        with open('user_password.txt') as f:
            username, password = f.readline().strip().split(':')
        con = mdb.connect('10.100.95.207', 'test', charset='utf8', use_unicode=True);
        with con:
            cur = con.cursor()
            cur.execute('SET NAMES utf8;')
            cur.execute('SET CHARACTER SET utf8;')
            cur.execute('SET character_set_connection=utf8;')
            sql_base = "INSERT INTO test.job_results (job_search_term, location_search_term, job_title, job_description) VALUES ('"
            sql_connector = "', '"
            sql_end = "')"
            sql_string = u''.join((sql_base, job_search_term.replace("'", ""), sql_connector, location_search_term.replace("'", ""), sql_connector, key.replace("'", ""), sql_connector, website_text.replace("'", "").replace('\n', ' '), sql_end)).encode('utf-8').strip()
            cur.execute(sql_string)


if __name__ == '__main__':
    args = get_arguments()
    indeed_scraper = job_search_runner(args.job_search_term, args.location_search_term)
    job_site_scraper = open_and_parse_job_websites()
    for key, value in indeed_scraper.job_dictionary.items():
        job_site_scraper.open_website(key, args.job_search_term, args.location_search_term, value)

