import time
import datetime
import mimetypes
import os.path

from django.conf import settings
from django.http import HttpResponse, Http404
from django.utils.http import http_date
from django.utils import cache
from django.utils.hashcompat import md5_constructor

import django_memorious


def memorious(request, name, revision=None, repository=None):
    if revision=="None":
        revision = None
        
    try:
        repo = django_memorious.get_repository(repository)
    except KeyError, e:
        raise Http404("No repository '%s'" % repository)

    repo_context = repo[revision]

    names = name.split("&")

    first_name = names[0]
    base = os.path.dirname(first_name)
    mimetype = mimetypes.guess_type(first_name)[0] or 'application/octet-stream'
    try:
        context = repo_context[first_name]
    except KeyError, e:
        raise Http404("No resource '%s'" % first_name)
    contents = context.data()

    for name in names[1:]:
        name = os.path.join("%s/" % base, name)
        # TODO: warn if mimetype of names[1:] is different from names[0]
        try:
            context = repo_context[name]
        except KeyError, e:
            raise Http404("No resource '%s'" % name)
        contents += context.data()
    
    response = HttpResponse(contents, mimetype=mimetype)

    response["Content-Length"] = len(contents)
    response["Cache-Control"] = "public"

    #  Cache
    if revision:
        #  cache for a long time
        WEEK = 60 * 60 * 24 * 7
        ttl = 52 * WEEK
    else:
        #  do not cache (revision may have been 'tip' or somesuch)
        ttl = 0
        response['ETag'] = '"%s"' % md5_constructor(response.content).hexdigest()

    response['Expires'] = http_date(time.time() + ttl)
    cache.patch_cache_control(response, max_age=ttl)

    return response
