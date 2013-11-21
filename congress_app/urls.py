from django.conf.urls import patterns, include, url
from congress_app import views

urlpatterns = patterns('congress_app.views',
    url(r'^votes/$', views.votes),
    url(r'^$', views.index),
)
