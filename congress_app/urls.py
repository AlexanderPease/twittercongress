from django.conf.urls import patterns, include, url

urlpatterns = patterns('congress_app.views',
    url(r'^$', 'index'),
    url(r'^results','results'),
    # url(r'^(?P<poll_id>\d+)/$', 'detail'),
   # url(r'^(?P<poll_id>\d+)/results/$', 'results'),
   # url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)
