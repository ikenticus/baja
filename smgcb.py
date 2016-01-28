from bottle import run, get, post, route, request, response, template, static_file
from couchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery
from lxml import etree
from pprint import pprint
import os
import random
import socket
import sys

COUCHBASE = 'couchbase://localhost'


@get('/query/word/<type>')
def get_word_type(type):
    cb = Bucket(COUCHBASE)
    # fails if you do not create an index on type
    #   $ /Applications/Couchbase\ Server.app/Contents/Resources/couchbase-core/bin/cbq
    #   cbq> CREATE PRIMARY INDEX ON default USING GSI;
    query = N1QLQuery("SELECT cnt, word, type FROM `default` WHERE type=$q_type", q_type=type)
    print query
    for row in cb.n1ql_query(query):
        print row


@get('/<project>/<service>.svc/<paths:path>')
def get_service(project, service, paths):
    try:
        params = paths.split('/')
        fixture = params[0].lower()
        module = __import__('%s.%s' % (project.lower(), service.lower()))
        svc = getattr(module, service.lower())
        action = getattr(svc, fixture)
        return action(params[1:])
    except ImportError:
        return { 'Error': 1, 'Message': 'Unable to load the %s SERVICE from the %s PROJECT' % (service, project) }
    except AttributeError:
        return { 'Error': 1, 'Message': 'Unable to handle %s FIXTURE in the %s SERVICE' % (paths.split('/')[0], service) }


#@get('/<bucket>/<doc:path>')
def get_document(bucket, doc):
    cb = Bucket(COUCHBASE + '/default')
    key = '%s_%s' % (bucket, doc.replace('/', '_'))
    #print key

    # randomly insert data
    put_documents(bucket, key)

    #couchbase.bucketmanager
    #design_create(name, ddoc, use_devmode=True, syncwait=0)

    # get odd views
    results = cb.query("dev_word", "Odd", limit=5)
    print results
    for row in results:
        print row

    # get exact document
    data = cb.get(key).value
    return data


def put_documents(bucket, key):
    cb = Bucket(COUCHBASE + '/default')
    for cnt in range(10):
        word = ''.join([chr(random.randint(97,122)) for r in range(0,random.randint(5,10))])
        if len(word) % 2 == 0:
            type = 'even'
        else:
            type = 'odd'
        d = { 'type': type, 'word': word, 'cnt': cnt }
        cb.upsert('%s_%02d' % (key, cnt), d)


def create_bucket(bucket):
    '''
        http://stackoverflow.com/questions/14513750/how-to-create-a-couchbase-bucket-using-python-client
    '''
    couchbase = Couchbase("127.0.0.1:8091", "Administrator", "password")
    # get the rest interface
    rest = couchbase._rest()
    rest.create_bucket(bucket='myBucket',
                        ramQuotaMB=160,
                        authType='sasl',
                        saslPassword='password',
                        replicaNumber=0,
                        bucketType='couchbase')


if __name__ == "__main__":
    port = 8080
    #host = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1][0]
    #run(host=host, port=port)
    run(port=port)
