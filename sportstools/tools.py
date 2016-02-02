import json
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

        # check for any feed overrides
        try:
            module = __import__('sportstools.%s' % bucket.lower())
            feed = getattr(module, bucket.lower())
            action = getattr(feed, fixture)
            return action(doc, params[:-1])

        # otherwise, default template processing
        except:
            templates = default_templates(params[:-1])
            data = parse_docs(doc, templates)
            key = '_'.join(params[1:-1])
            if data:
                upsert_document(DEFBUCKET, key, json.loads(data))
    else:
        return { 'Message': 'Load failed, empty or missing doc' }

