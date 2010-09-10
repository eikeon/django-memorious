from django.conf.urls.defaults import patterns, url, include

from test_project import views

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'


urlpatterns = patterns(
    '',

    url(r'^$', views.home, name="home"),

    (r'^', include('django_memorious.urls')),

)
