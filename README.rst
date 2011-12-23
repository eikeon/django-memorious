django-memorious - django application for dealing with static resources
=======================================================================

django application for dealing with static resources regarding urls,
cache headers, and versions.


Features
--------

* template tag for generating versioned urls for static resources.

* url pattern and view for serving up the versioned urls

* support for multiple repo types. currently git, hg, and 'no
  repository'.

* support for multiple repos at a time.

* MEMORIOUS_DEBUG flag for serving up uncached version of the static
  resources useful while developing the resources.


Installation
------------

You can install django-memorious with the command::

  $ pip install https://github.com/eikeon/django-memorious/tarball/master

and the prerequisites::

  $ pip install mercurial
  $ pip install GitPython
  $ pip install Django


Example usage
-------------

add the following bits to your settings.py::

  INSTALLED_APPS += (
      'django_memorious',
  )

  MEMORIOUS_REPOSITORIES = {
      "default": "/path/to/repo_containing_static_resources"
      }

  MEMORIOUS_DEBUG = True

include the django_memorious.urls in your urlpatters, for example::

  (r'^', include('django_memorious.urls')),

  or

  (r'^media/', include('django_memorious.urls')),  

in your templates::

  {% load memorious %}

  <a href="{% memorious 'css/site.css' %}">...</a>


Source
------

http://github.com/eikeon/django-memorious/
