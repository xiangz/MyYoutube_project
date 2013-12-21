from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from myYoutube.views import one_time
# one_time_startup()
# W =444
# settings.V=W


admin.autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# settings.variable=want
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MyYoutube_project.views.home', name='home'),
    # url(r'^MyYoutube_project/', include('MyYoutube_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ratings/', include('ratings.urls')),
    url(r'^myYoutube/',include('myYoutube.urls') ),
    url(r'^admin/', include(admin.site.urls)), # ADD THIS LINE


)
one_time()
