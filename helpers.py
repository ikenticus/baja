import os

from couchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery
from jinja2 import Template

COUCHBASE = 'couchbase://localhost'
DEFBUCKET = 'sports'
TEMPLATES = 'tpl'


def upsert_document (bucket, key, doc):
    cb = Bucket(COUCHBASE + '/' + bucket)
    cb.upsert(key, doc)



def default_templates (params):
    '''
        Default template list: bucket/fixture/sport/league[/event][/team]/key
    '''
    templates = []
    feed = params[0]
    for end in range(len(params), 1, -1):
        templates.append('%s/%s/%s.tpl' % (TEMPLATES, feed, '_'.join(params[1:end])))
    return templates


def parse_docs (doc, templates):
    for tplfile in templates:
        if os.path.exists(tplfile):
            template = Template(open(tplfile).read())
            return template.render(doc=doc)


#@get('/query/word/<type>')
def get_word_type (type):
    cb = Bucket(COUCHBASE)
    # fails if you do not create an index on type
    #   $ /Applications/Couchbase\ Server.app/Contents/Resources/couchbase-core/bin/cbq
    #   cbq> CREATE PRIMARY INDEX ON default USING GSI;
    query = N1QLQuery("SELECT cnt, word, type FROM `default` WHERE type=$q_type", q_type=type)
    print query
    for row in cb.n1ql_query(query):
        print row
