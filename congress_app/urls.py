from django.conf.urls import patterns, include, url
from congress_app import views

urlpatterns = patterns('congress_app.views',
    url(r'^votes/$', views.votes),
    url(r'^tweet/$', views.tweet),
    url(r'^scratch/$', views.scratch),
    url(r'^$', views.index),
)


    #url(r'', include('social_auth.urls')), not working

    # user auth urls 
    #url(r'^accounts/login/$', 'congress_app.views.login'),
    #url(r'^accounts/auth/$', 'congress_app.views.auth_view'),
    #url(r'^accounts/logout/$', 'congress_app.views.logout'),
    #url(r'^accounts/loggedin/$', 'congress_app.views.loggedin'),
    #url(r'^accounts/invalid/$', 'congress_app.views.invalid_login'),