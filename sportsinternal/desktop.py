from helpers import *


def transactions (params=None):
    cb = Bucket(COUCHBASE + '/sports')
    query = {
        'fixture': 'transactions',
        'league_name': params[0]
    }
    team = params[-1]
    data = query_sports(query)
    if data:
        if len(data) > 1:
            return { 'Message': 'Multiple transactions found!' }
        else:
            return data[0]
    else:
        return { 'Message': 'No transactions found!' }



