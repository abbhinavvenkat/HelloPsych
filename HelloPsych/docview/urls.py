from django.conf.urls import patterns, url
from docview.views import   \
    profile, dashboard, slot, profile_update, \
    history, specialization, profile_create, stat

urlpatterns = patterns('',
    url(r'^history/$', history, name='history'),
    url(r'^dashboard/(?P<doc>\w+)/$', dashboard, name='dashboard'),
    url(r'^timeslot$', slot, name='slot'),
    url(r'^stat$', stat, name='stat'),
    url(r'^edit$', profile_update, name='edit'),
    url(r'create$', profile_create, name='create'),
    url(r'^specialization$', specialization, name='specialization'),
    url(r'^(?P<doc>\w+)/$', profile, name='profile'),
)
