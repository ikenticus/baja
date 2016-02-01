
def load(params=None):
    '''
        Load feed documents into database
    '''
    bucket = params[0].lower()
    fixture = params[1].lower()
    module = __import__('sportstools.%s' % bucket.lower())
    feed = getattr(module, bucket.lower())
    action = getattr(feed, fixture)
    return action(params[2:])
