import MySQLdb as mdb
import manual_tfidf


def what_words_am_i_missing(cv, job_ids):
    job_descriptions = get_docs_by_job_id(job_ids)
    important_words_freqs = manual_tfidf.new_run_tfidf(job_descriptions)
    important_words = [word for (word, freq) in important_words_freqs]
    for word in important_words:
        if word not in cv:
            print word

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

what_words_am_i_missing(["cat", "foo", "dog", "bright", "concept"], [1,2,3])
