import datetime
from django import template
from django.conf import settings
from django.core import urlresolvers

from mercurial import node


register = template.Library()


class MemoriousNode(template.Node):
    _cache = {}

    def __init__(self, repository, path):
        self.repository = repository
        self.path = path

    def render(self, context):
        url = self._cache.get(self.path, None)
        if not url:
            repo = settings.MEMORIOUS_REPOSITORIES[self.repository]
            changectx = repo['tip']
            fctx = changectx[self.path]
            url = urlresolvers.reverse(
                'memorious', 
                kwargs={"repository": self.repository,
                        "revision": fctx.hex(), #.filerev(),
                        "name": self.path})
            self._cache[self.path] = url
        return url


@register.tag(name="memorious")
def parse_memorious(parser, token):
    try:
        args = token.contents.split()
        tag_name = args[0]
        path = args[1]
        if len(args)>=3:
            repository = args[2]
        else:
            repository = "'default'"
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % tag_name)
    if repository[0] == repository[-1] and repository[0] in ('"', "'"):
        repository = repository[1:-1]
    else:
        raise template.TemplateSyntaxError(
            "%r tag's arguments should be in quotes" % tag_name)
    if path[0] == path[-1] and path[0] in ('"', "'"):
        path = path[1:-1]
    else:
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name)
    return MemoriousNode(repository, path)
