import os

import mercurial.hg
import mercurial.ui

import git

from django.conf import settings


class NoRepo(object):
    def __init__(self, directory):
        self._directory = directory

    def __getitem__(self, revision):
        if revision != None:
            raise Exception("revision specified on NoRepo")
        else:
            return NoRevision(self._directory)

    @property
    def current_revision(self):
        return "None"


class NoRevision(object):
    def __init__(self, directory):
        self._directory = directory

    def __getitem__(self, path):
        return NoItem(os.path.join(self._directory, path))


class NoItem(object):
    def __init__(self, path):
        self._path = path

    def data(self):
        return open(self._path, "rb").read()


class GitRepo(object):
    def __init__(self, directory):
        self._repo = git.repo.base.Repo(directory)

    def __getitem__(self, revision):
        # return GitRevision(self._repo.tree(revision))
        #
        # The above gets us the tree, but we run into problems when we
        # try to use it. So, we've followed the advice from the
        # documentation noted below.
        #
        # Note: If you need a non-root level tree, find it by
        # iterating the root tree. Otherwise it cannot know about its
        # path relative to the repository root and subsequent
        # operations might have unexpected results.
        for tree in self._repo.iter_trees():
            if tree.hexsha==revision:
                return GitRevision(tree)
        else:
            raise Exception("revision '%s' not found" % revision)

    @property
    def current_revision(self):
        changectx = self._repo.tree("HEAD")
        return changectx.hexsha


class GitRevision(object):
    def __init__(self, tree):
        self._tree = tree

    def __getitem__(self, path):
        return GitItem(self._tree.__getitem__(path))


class GitItem(object):
    def __init__(self, item):
        self._item = item

    def data(self):
        return self._item.data_stream.read()


class HGRepo(object):
    def __init__(self, directory):
        self._repo = mercurial.hg.repository(mercurial.ui.ui(), directory)

    def __getitem__(self, revision):
        return self._repo.__getitem__(revision)

    @property
    def current_revision(self):
        changectx = self._repo['tip']
        return changectx.hex()


class HGRevision(object):
    def __init__(self, context):
        self._context = context

    def __getitem__(self, path):
        return HGItem(self._context.__getitem__(path))


class HGItem(object):
    def __init__(self, item):
        self._item = item

    def data(self):
        return self._item.data()

_cache = {}

def get_repository(name):
    repo = _cache.get(name, None)
    if not repo:
        directory = settings.MEMORIOUS_REPOSITORIES[name]
        if getattr(settings, "MEMORIOUS_DEBUG", False):
            repo = NoRepo(directory)
        else:
            try:
                repo = GitRepo(directory)
            except:
                try:
                    repo = HGRepo(directory)
                except:
                    raise Exception("Could not open repository from directory %s" % directory)
        _cache[name] = repo
    return repo
