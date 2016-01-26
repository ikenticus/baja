from bottle import run, get, post, route, request, template, static_file
from couchbase.bucket import Bucket
from lxml import etree
from pprint import pprint
import os
import socket
import sys

COUCHBASE = 'couchbase://localhost/'

@get('/<bucket>/<doc:path>')
def get_document(bucket, doc):
    d = { 'which': 'way', 'but': 'down' }
    key = '%s_%s' % (bucket, doc.replace('/', '_'))
    #print key
    cb = Bucket(COUCHBASE + 'default')
    #cb.upsert(key, d)
    return cb.get(key).value


'''
    Main
'''
port = 8080
#host = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1][0]
#run(host=host, port=port)
run(port=port)
