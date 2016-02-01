from helpers import *


def dump (params=None):
    feed, key = params[0:2]
    cb = Bucket(COUCHBASE + '/' + feed)
    doc = cb.get(key).value
    return doc


def load (params=None, doc=None):
    '''
        Load feed documents into database
    '''
    if doc:
        key = params[-1].lower()
        bucket = params[0].lower()
        fixture = params[1].lower()
        upsert_document(bucket, key, doc)
        module = __import__('sportstools.%s' % bucket.lower())
        feed = getattr(module, bucket.lower())
        action = getattr(feed, fixture)
        return action(params[2:])

