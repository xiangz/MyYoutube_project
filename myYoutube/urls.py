from django.conf.urls import patterns,url
from myYoutube import views

urlpatterns = patterns('',
          url(r'^$', views.index,name='index' ),
          url(r'^deleteVideo/$',views.deleteVideo,name='deleteVideo'),
          url(r'^watch/$',views.watch,name='watch'),

        )