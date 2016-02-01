from bottle import run, get, post, route, request, response, template, static_file
from lxml import etree
from pprint import pprint
import bottle
import json
import os
import random
import socket
import sys

bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 * 10


@post('/<project>/<service>.svc/<paths:path>')
def post_service (project, service, paths):
    try:
        params = paths.split('/')
        fixture = params[0].lower()
        module = __import__('%s.%s' % (project.lower(), service.lower()))
        svc = getattr(module, service.lower())
        action = getattr(svc, fixture)
        return action(params[1:], json.loads(request.body.read()))
    except ImportError:
        return { 'Error': 1, 'Message': 'Unable to load the %s SERVICE from the %s PROJECT' % (service, project) }
    except AttributeError:
        return { 'Error': 1, 'Message': 'Unable to handle %s FIXTURE in the %s SERVICE' % (paths.split('/')[0], service) }



@get('/<project>/<service>.svc/<paths:path>')
def get_service (project, service, paths):
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


if __name__ == "__main__":
    port = 8080
    #host = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1][0]
    #run(host=host, port=port)
    run(port=port)
