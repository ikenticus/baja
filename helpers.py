
from couchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery

COUCHBASE = 'couchbase://localhost'


def upsert_document (bucket, key, doc):
    cb = Bucket(COUCHBASE + '/' + bucket)
    cb.upsert(key, doc)


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
