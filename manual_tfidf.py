#!/usr/bin/python
from __future__ import division, unicode_literals
import math
from text.blob import TextBlob as tb
import MySQLdb as mdb

word_dictionary = {}
wordy_dictionary = {}
document_dictionary = {}

def n_containing(word, documentlist):
    return sum(1 for document in documentlist if word in document.split(' '))

def populate_document_dictionary(documentlist):
    """
    For TF
    """
    document_dictionary = {}
    for document_index in range(len(documentlist)):
        word_count = 0
        document_dictionary[document_index] = {}
        for word in documentlist[document_index].split(' '):
            word_count += 1
            if word not in document_dictionary[document_index]:
                document_dictionary[document_index][word] = 1
            else:
                document_dictionary[document_index][word] += 1
        document_dictionary[document_index]['count'] = word_count
    return document_dictionary

def tf(word, document):
    count = len([my_word for my_word in document.split(' ') if my_word == word])
    return count / len(document)

def new_tf(word,index, useful_dictionary):
    if index not in useful_dictionary:
        print "Don't know why but %s is not in the dictionary" % str(index)
    if word in useful_dictionary[index]:
        count = useful_dictionary[index][word]
    else:
        count = 0
    word_count = useful_dictionary[index]['count']
    return float(count)/word_count

def populate_containing_dictionary(documentlist):
    """
    For IDF
    """
    wordy_dictionary = {}
    for document_index in range(len(documentlist)):
        for word in documentlist[document_index].split(' '):
            if word in wordy_dictionary:
                wordy_dictionary[word].append(document_index)
            else:
                wordy_dictionary[word] = [document_index]
    return wordy_dictionary

def new_idf(word, useful_dictionary, documentlist):
    return math.log(len(documentlist)/(1 + len(useful_dictionary[word])))

def idf(word, documentlist):
    return math.log(len(documentlist) / (1 + n_containing(word, documentlist)))

def tfidf(word, document, documentlist):
    return tf(word, document) * idf(word, documentlist)

def new_tfidf(word, index, document_dictionary,idf_dictionary,documentlist):
    return new_idf(word, idf_dictionary, documentlist) * new_tf(word, index, document_dictionary)

def run_tfidf(document_list):
    documentlist = [tb(document) for document in document_list]
    for i, document in enumerate(documentlist):
        print "Top words in document %s" % str(int(i) + 1)
        scores = dict((word, tfidf(word, document, documentlist)) for word in document.split(' '))
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:5]:
            print "Word: %s, TF-IDF: %s" % (str(word), str(score))


def new_run_tfidf(document_list):
    documentlist = [tb(document) for document in document_list]
    document_dictionary = populate_document_dictionary(documentlist)
    idf_dictionary = populate_containing_dictionary(documentlist)
    for i, document in enumerate(documentlist):
        print "Top words in document %s" % str(int(i) + 1)
        scores = dict((word, new_tfidf(word,int(i),document_dictionary,idf_dictionary, documentlist)) for word in document.split(' '))
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:5]:
            print "Word: %s, TF-IDF: %s" % (str(word), str(score))
