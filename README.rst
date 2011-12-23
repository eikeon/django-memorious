django-memorious - django application for dealing with static resources
=======================================================================

django application for dealing with static resources regarding urls,
cache headers, and versions.


Features
--------

* template tag for generating urls for static resources that contain
  their version info.

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


Example usage
-------------

add the following bits to your settings.py::

  INSTALLED_APPS += (
      'django_memorious',
  )

  MEMORIOUS_REPOSITORIES = {
      "default": "/path/to/repo"
      }

  MEMORIOUS_DEBUG = True

include the django_memorious.urls in your urlpatters, for example::

  (r'^', include('django_memorious.urls')),

  or

  (r'^media/', include('django_memorious.urls')),  


Source
------

The source code is currently available on github. Fork away!

http://github.com/eikeon/django-memorious/
