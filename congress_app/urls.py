from django.conf.urls import patterns, include, url

urlpatterns = patterns('congress_app.views',
    url(r'^$', 'index'),
)
