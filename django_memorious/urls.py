from django.conf.urls.defaults import patterns, url

from django_memorious import views


urlpatterns = patterns(
    'django_memorious',

    url(r'^(?P<repository>[^-]+)-(?P<revision>[^/]+)?/(?P<name>.*)$',
        views.memorious, name="memorious"),

)

