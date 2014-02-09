#!/usr/bin/python
import re
import manual_tfidf
try:
  import cv_comparer
except:
  print "fucking macs"
import pdfPathToText
import json
import pickle
#from manual_tfidf import populate_document_dictionary, populate_containing_dictionary
#from cv_comparer import run_query, populate_doc_weights, best_matches_fast, getVector
#from pdfPathToText import convert_pdf_to_txt

def get_job_by_id(jid):
  """
  Method was desired to get a job without instantiating a full jobSearch object
  as it makes a big ass dictionary
  """
  sql_query = "SELECT * FROM test.job_results WHERE search_id = " + str(jid)
  return dict((job_id, {'job_id': job_id, 'search_term' : search.decode('utf-8', 'ignore'), 'location_term' : location.decode('utf-8', 'ignore'), 'job_title' : title.decode('utf-8', 'ignore'), 'job_description' : description.decode('utf-8', 'ignore')}) for (job_id, search, location, title, description) in cv_comparer.run_query(sql_query))

class jobSearch(object):

    def __init__(self):
        return
        self.job_dictionary = self.get_all_job_info()
        self.job_description_list = [self.procText(self.job_dictionary[entry]['job_description']) for entry in self.job_dictionary.keys()]

        # self.tf_dictionary = populate_document_dictionary(self.job_description_list) # is this needed anywhere?
        self.df_dictionary = manual_tfidf.populate_containing_dictionary(self.job_description_list)
        self.doc_weights = cv_comparer.populate_doc_weights(self.job_description_list, self.df_dictionary, len(self.job_description_list)) #list of weights, same index as docList

    def procText(self, desc):
      fDesc = re.sub(r'[^a-zA-Z0-9_\'-]+', ' ', desc.lower())
      return fDesc.split()

    def get_all_job_info(self):
        sql_query = "SELECT * FROM test.job_results"
        return dict((job_id, {'job_id': job_id, 'search_term' : search.decode('utf-8', 'ignore'), 'location_term' : location.decode('utf-8', 'ignore'), 'job_title' : title.decode('utf-8', 'ignore'), 'job_description' : description.decode('utf-8', 'ignore')}) for (job_id, search, location, title, description) in cv_comparer.run_query(sql_query))

    def get_job_info(self, job_id):
        return self.job_dictionary.get(job_id, None)

    def get_related_jobs(self, cv, noResults=6):
        pcv = self.procText(cv)
        return cv_comparer.best_matches_fast(pcv, self.doc_weights, self.df_dictionary, len(self.job_description_list), noResults)

    def get_json_job_info(self, job_id):
        return json.dumps(self.job_dictionary.get(job_id, None), ensure_ascii=False)

    def return_missing_words(self, cv, job_list):
        jobs_descriptions = []
        for job_id in job_list:
          jobs_descriptions.append(self.get_job_info(job_id))
        important_word_freqs = manual_tfidf.run_tfidf(jobs_descriptions)
        important_words = [(word, freq) for (word, freq) in important_word_freqs if word not in cv]
        return important_words

    def get_pdf_as_text(self, path_to_pdf):
        return pdfPathToText.convert_pdf_to_txt(path_to_pdf)
    
    def readCVs(self, path):
        with open(path, 'r') as f:
            self.bizExp, self.edu, self.job, self.company, self.name, self.email, self.phoneNumber, self.cvCount = pickle.load(f)
        print map(type, (self.bizExp, self.edu, self.job, self.company, self.name, self.email, self.phoneNumber, self.cvCount))
        self.dispCV = []
        for i in range(len(self.bizExp)):
          self.dispCV.append([self.bizExp[i], self.edu[i], [], [], [], [], []])
          for (k,v) in self.job.items():
            if i in v:
              self.dispCV[i][2].append(k)
          for (k,v) in self.company.items():
            if i in v:
              self.dispCV[i][3].append(k)
          for (k,v) in self.name.items():
            if i in v:
              self.dispCV[i][4].append(k)
          for (k,v) in self.email.items():
            if i == v:
              self.dispCV[i][5].append(k)
          for (k,v) in self.phoneNumber.items():
            if i in v:
              self.dispCV[i][6].append(k)

    def initCVs(self, read = None):
        if not read:
            self.cvList = [self.procText(self.bizExp[cv_index] + " " + self.edu[cv_index]) for cv_index in range(len(self.bizExp))]
        else:
            self.cvList = [self.procText(r) for r in read]
        self.cvDfs = manual_tfidf.populate_containing_dictionary(self.cvList)
        self.cvWeights = cv_comparer.populate_doc_weights(self.cvList, self.cvDfs, len(self.cvList))

    def getBlob(self, inds):
      return self.concat([self.cvList[i] for i in inds])

    def getImpWords(self, query, noWords):
      query = query.lower()
      inds = list(self.parseSearch(query, [self.job, self.company]))
      blob = self.getBlob(inds)
      vec = cv_comparer.getVector(blob, self.cvDfs, len(self.cvList), tp=None)
      #print sorted(vec.items(), key=lambda x: x[1], reverse=True)
      return map(lambda x:x[0], sorted(vec.items(), key=lambda x: x[1], reverse=True)[:noWords])

    def getRelCVs(self, query):
      query = query.lower()
      inds = list(self.parseSearch(query, [self.job, self.company]))
      return [self.bizExp[i] for i in inds]

    def searchWord(self, word, dicts):
        inds = set([])
        for d in dicts:
            for (k,v) in d.items():
              if word in k.lower().split():
                inds = inds.union(set(v))
            return inds

    def parseSearch(self, query, dicts):
      if '&' in query:
        (f,s) = query.split('&',1)
        inds = self.parseSearch(f, dicts)
        inds = inds.intersection(self.parseSearch(s,dicts))
        return inds
      elif ' ' in query:
        (f,s) = query.split(' ',1)
        inds = self.parseSearch(f, dicts)
        inds = inds.union(self.parseSearch(s,dicts))
        return inds
      else:
        return self.searchWord(query, dicts)

    def concat(self,lists):
        rez = []
        for l in lists:
          rez += l
        return rez

    def testImpWords(self):
      cvs = [""]
      split = False
      ind = 0
      with open("MBA_2014.txt",'r') as f:
        for line in f:
          if split:
            ind += 1
            split = False
            cvs.append("")
          if line[:11] == "NATIONALITY":
            split = True
          cvs[ind] += line + '\n'

      #print '\n----------------------\n'.join(cvs)
      return cvs

if __name__ == "__main__":
  """
  cvs = testImpWords()
  x = jobSearch()
  x.initCVs(cvs)
  inds = [i for i in range(len(cvs)) if "trader" in cvs[i].lower()]
  print inds
  print x.getImpWords(inds, 50)
  """
  j = jobSearch()
  j.readCVs('CVs/MiF_2014_data.pickle')
  print j.dispCV
  #print j.job
  #print j.company
  j.initCVs()
  print j.getImpWords("trader",50)
  #print j.getRelCVs("trader")
#  cv_as_string = j.get_pdf_as_text('MattGaming.pdf')
#  for job_id in j.get_related_jobs(cv_as_string):
#      json_job_information = j.get_json_job_info(job_id)
#      print json_job_information
#  dicts = [{'abra cada bra':[1,2,3,4,5], 'qui':[3,7,9,10], 'pui':[3,4,5,6,7]},{'lui':[2,3,4,9],'cui':[1,8,5,10]}]
#  print j.parseSearch("qui & pui",dicts)
