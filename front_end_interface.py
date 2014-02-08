#!/usr/bin/python

from manual_tfidf import populate_document_dictionary, populate_containing_dictionary
from cv_comparer import run_query

class jobSearch(object):

    def __init__(self):
        self.job_dictionary = self.get_all_job_info()
        self.job_description_list = [self.job_dictionary[entry]['job_description'] for entry in self.job_dictionary.keys()]
        self.tf_idf_document_dictionary = populate_document_dictionary(self.job_description_list)
        self.tf_idf_word_frequency_dictionary = populate_containing_dictionary(self.job_description_list)


    def get_all_job_info(self):
        sql_query = "SELECT * FROM test.job_results"
        return dict((job_id, {'search_term' : search.decode('utf-8', 'ignore'), 'location_term' : location.decode('utf-8', 'ignore'), 'job_title' : title.decode('utf-8', 'ignore'), 'job_description' : description.decode('utf-8', 'ignore')}) for (job_id, search, location, title, description) in run_query(sql_query))

    def get_job_info(self, job_id):
        return self.job_dictionary.get(job_id, None)
    
    def get_related_jobs(self, cv, number_of_results=6):
        ## tokenize cv
        ## perform cosine similarity on self.tf_idf_vectors
        ## return indices of max

    def return_missing_words(self, cv, job_list):
        ## Get top words from job_list
        ## Compare to cv
        ## Return the diff

x = jobSearch()
