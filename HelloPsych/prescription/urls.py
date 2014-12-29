from django.conf.urls import patterns, url
from prescription.views import prescribe, prescriptions

urlpatterns = patterns('',
    url(r'^prescribe/(?P<req_id>\d+)/(?P<med_count>\d+)/$', \
    	prescribe, name='prescribe'),
    url(r'^prescriptions/(?P<prescription_id>\d+)$', \
        prescriptions, name='prescriptions'),
)
