import time
import datetime
import mimetypes

from django.conf import settings
from django.http import HttpResponse
from django.utils.http import http_date
from django.utils import cache

import django_memorious


def memorious(request, name, revision=None, repository=None):
    if revision=="None":
        revision = None
        
    repo = django_memorious.get_repository(repository)

    if revision==None:
        context = repo[revision][name]
    else:
        changectx = repo[revision]
        context = changectx[name]

    mimetype = mimetypes.guess_type(name)[0] or 'application/octet-stream'
    contents = context.data()
    response = HttpResponse(contents, mimetype=mimetype)

    timestamp, offset = context.date()
    modified = datetime.datetime.fromtimestamp(timestamp)
    modified += datetime.timedelta(0, offset)
    response["Last-Modified"] = http_date(time.mktime(modified.timetuple()))

    response["Content-Length"] = len(contents)

    #  Cache
    if revision:
        #  cache for a long time
        WEEK = 60 * 60 * 24 * 7
        ttl = 2 * WEEK
    else:
        #  do not cache (revision may have been 'tip' or somesuch)
        ttl = 0
    cache.patch_response_headers(response, ttl)

    return response

