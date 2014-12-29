from django.conf.urls import patterns, include, url
from patientview.views import *

urlpatterns = patterns('',
     url(r'^$', home, name='patient'),
     url(r'home', index),
     url(r'^help/$', help, name='help'),
     url(r'^help/issue/$', issue, name='issue'),
     url(r'index/$', index, name='index'),
     url(r'index_init/$', index_init, name='index_init'),
     url(r'notify/$', notify, name='notify'),
     url(r'director/$', director),
     url(r'fixcall/(?P<did>\d+)/$', fix, name="fixcall"),
     url(r'broadcast$', iFix, name="iFix"),
     url(r'index_search/$', index_search, name='index_search'),
     url(r'buy/$', buy, name='buy'),
     url(r'history/$', history, name='history'),
)
