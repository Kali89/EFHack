#!/usr/bin/python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity 
import numpy as np
import nltk
import MySQLdb as mdb
import sys
import argparse
from argparse import ArgumentParser
import os.path
import math
import front_end_interface 
#import front_end_interface
#from manual_tfidf import run_tfidf, tfidf

### Grab their CV and split it up
def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s doesn't exist!" % arg)
    else:
        return arg

def run_query(sql_statement):
    with open('user_password.txt') as f:
        username, password = f.readline().strip().split(':')
    con = mdb.connect('10.100.95.207', username, password, 'test');
    with con:
        cur = con.cursor()
        cur.execute(sql_statement)
        return cur.fetchall()


def get_similar_documents(original_document_id, similarity_matrix, number_of_documents):
    similar_documents = similarity_matrix[original_document_id].argsort()[:-number_of_documents - 1:-1]
    return [original_document_id, similar_documents]


def parse_cv(filepath):
    with open(filepath, 'rb') as f:
        cv = ' '.join(f.readlines())
    return cv.replace('\n', ' ').strip()

def parse_arguments():
    parser = ArgumentParser(description='Get a CV')
    parser.add_argument('-i', dest="filename", required=True, metavar='FILE', help="input path to cv", type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()
    return args

## Find similarity matrix between job postings
def make_similarity_matrix(all_jobs_dictionary):
    job_list_without_cv = [all_jobs_dictionary[key].decode('utf-8', 'ignore') for key in all_jobs_dictionary.keys()] 
    job_list_without_cv_tfidf = TfidfVectorizer().fit_transform(job_list_without_cv)
    similarity_matrix = (job_list_without_cv_tfidf * job_list_without_cv_tfidf.T).A
    return similarity_matrix

## Find the best 3 documents for the CV
def best_matches(cv, all_jobs_dictionary, index_dictionary, number_of_results):
    all_jobs_dictionary[0] = cv.lower()
    job_list_to_tfidf = [all_jobs_dictionary[key].decode('utf-8', 'ignore').lower() for key in all_jobs_dictionary.keys() if isinstance(all_jobs_dictionary[key], str)] 
    job_list_tfidf = TfidfVectorizer().fit_transform(job_list_to_tfidf)
    cosine_similarities = cosine_similarity(job_list_tfidf[0:1], job_list_tfidf).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-number_of_results - 1:-1]
    actual_indices = [index_dictionary[index] for index in related_docs_indices if index != 0]
    return actual_indices

def populate_doc_weights(docList, df, N):
  weights = []
  for i in range(len(docList)):
    weights.append(getVector(docList[i], df, N))
  return weights

def best_matches_fast(query, docWeights, df, N, noResults):
  qVec = getVector(query, df, N)
  scores = []
  for i in range(len(docWeights)):
    scores.append((dotProd(qVec, docWeights[i]), i))

  sScores = sorted(scores, reverse=True)
  return [i for (s,i) in sScores[:noResults]]
  
def dotProd(v1, v2):
  #checkNorm(v1)
  #checkNorm(v2)
  prod = 0
  for (w,s) in v1.items():
    if w in v2:
      prod += s*v2[w]
  return prod

def getVector(query, df, N, tp=None):
  tf = getTF(query)
  vec = {}
  for word in query:
    if not word in df:
      continue
    if tp != None:
      print word, tf[word], len(df[word]), N, calcWeight(tf[word], len(df[word]), N)
    vec[word] = calcWeight(tf[word], len(df[word]), N)

  return normalize(vec)

def calcWeight(tf, df, N):
  tfw = tf
  idfw = math.log(N/(1.0+df))
  return tfw*idfw

def getTF(query):
  tf = {}
  for word in query:
    try:
      tf[word] += 1
    except:
      tf[word] = 1
  return tf

def normalize(a):
  factor = math.sqrt(sum([x*x for x in a.values()]))
  return dict([(k, x/factor) for (k, x) in a.items()])

def checkNorm(a):
  assert(abs(sum([x*x for x in a.values()]) - 1) < 0.0001)

#if __name__ == "__main__":
#  testDoc = 'test_document.txt'
#  with open(testDoc, 'r') as f:
#    testContents = f.read()
#
#  #print parse_cv(testDoc)
#  #print front_end_interface.jobSearch().procText(testContents)
#
#  ## Get all the jobs out of the database
#  all_jobs_dictionary = dict((line[0], line[1].strip().replace('\n', ' ')) for line in run_query('SELECT search_id, job_description from test.job_results') if len(line[1].strip().replace('\n', ' ').split(' ')) > 30 )
#  i = 0
#  index_dictionary = {}
#  for line in run_query('SELECT search_id, job_description from test.job_results'):
#      if len(line[1].strip().replace('\n', ' ').split(' ')) > 30:
#          i += 1
#          index_dictionary[i] = line[0]
#      else:
#          index_dictionary[i] = False
#
#  related_doc_indices = best_matches(parse_cv(testDoc), all_jobs_dictionary, index_dictionary, 4)
#  print related_doc_indices
#
#  j = front_end_interface.jobSearch()
#
#  print best_matches_fast(j.procText(testContents), j.doc_weights, j.df_dictionary,len(j.job_description_list), 4)

## Show the 'customer' title and description on all 3 jobs
#useful_dictionary = dict(get_similar_documents(item, similarity_matrix, 5) for item in related_docs_indices[1:])
#
## Let the person pick one - use the 5 most similar documents to that one to show them

## If we've got nothing similar either:
#a) prompt the user for a search term - use this to populate the database and repeat
#b) take the top 5 rated terms in the users CV and use them to search then repeat


