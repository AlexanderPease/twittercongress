from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('congress_app.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # user auth urls 
    '''
    url(r'^accounts/login/$', 'congress_app.views.login'),
    url(r'^accounts/auth/$', 'congress_app.views.auth_view'),
    url(r'^accounts/logout/$', 'congress_app.views.logout'),
    url(r'^accounts/loggedin/$', 'congress_app.views.loggedin'),
    url(r'^accounts/invalid/$', 'congress_app.views.invalid_login'),
    '''
)

urlpatterns += staticfiles_urlpatterns()

