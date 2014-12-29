from django.conf.urls import patterns, include, url
from messageapp.views import *

urlpatterns = patterns('',
     url(r'inbox/$',inbox,name='inbox'),
     url(r'^msg/(?P<msg_id>\w+)/$', particular_msg, name='particular_msg'),
)
