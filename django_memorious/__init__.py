import mercurial.hg
import mercurial.ui

from django.conf import settings


_cache = {}

def get_repository(name):
    repo = _cache.get(name, None)
    if True or not repo:
        directory = settings.MEMORIOUS_REPOSITORIES[name]
        repo = _cache[name] = mercurial.hg.repository(mercurial.ui.ui(), directory)
    return repo
