from django.conf.urls import patterns, url

from message_reader import views

urlpatterns = patterns('',
             
  ############
  #Page views#
  ############
  
  #points to the main page view
  url(r'^$', views.index, name='index'),
  url(r'^messages/$', views.messages, name='messages'),
  
 
 )