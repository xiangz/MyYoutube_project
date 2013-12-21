from django.conf.urls import patterns,url
from myYoutube import views

urlpatterns = patterns('',
          url(r'^$', views.index,name='index' ),
          url(r'^deleteVideo/$',views.deleteVideo,name='deleteVideo'),
          url(r'^watch/$',views.watch,name='watch'),
          url(r'^register/$',views.register,name='register'),
          url(r'^login/$', views.user_login, name='login'),
          url(r'^logout/$', views.user_logout, name='logout'),
        )