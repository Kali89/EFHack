#!/usr/bin/python

import web
import cv_comparer
import json

def make_text(string):
    return string.encode('ascii', 'ignore')

urls = (
    '/', 'index', 
    '/about', 'about',
    '/contact', 'contact'
)

home_render = web.template.render('templates/')

app = web.application(urls, globals())

my_form = web.form.Form(web.form.Textarea('content', class_='textfield', id='textfield', rows=20, columns=60, description='Post your CV in here:'),)

jobs_dictionary = dict((line[0], line[1].strip().replace('\n', ' ')) for line in cv_comparer.run_query('SELECT search_id, job_description FROM test.job_results') if len(line[1].strip().replace('\n', ' ').split(' ')) > 15)
i = 0
index_dictionary = {}
for line in cv_comparer.run_query('SELECT search_id, job_description from test.job_results'):
    if len(line[1].strip().replace('\n', ' ').split(' ')) > 15:
        i += 1
        index_dictionary[i] = line[0]
    else:
        index_dictionary[i] = False

#similarity_matrix = make_similarity_matrix(all_jobs_dictionary)

class index:
    def GET(self):
        form = my_form()
        return home_render.index(form, "Paste your CV in here: ")

    def POST(self):
        input_string = web.input()
        try:
            cv = make_text(input_string['content'])
        except:
            cv = make_text(input_string['textfield'])
        related_docs = cv_comparer.best_matches(cv, jobs_dictionary, index_dictionary, 7)
        job_info = [cv_comparer.run_query("SELECT job_title, job_description FROM test.job_results WHERE search_id = " + str(search_id)) for search_id in related_docs[1:]]
        title_description = dict((entry[0][0], entry[0][1]) for entry in job_info if entry)
        web.header('Content-Type', 'application/json')
        #similarity_matrix = dict((item,best_matches(item, all_jobs_dictionary, 6)) for item in related_docs[1:])
        return json.dumps(title_description, ensure_ascii=False)

class contact:
    def GET(self):
        return home_render.contact()

class about:
    def GET(self):
        return home_render.about()
    
if __name__ == '__main__':
    app.run()

