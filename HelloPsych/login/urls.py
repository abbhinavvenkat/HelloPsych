from django.conf.urls import patterns, include, url
from login.views import *
from login.forms import *
from django.contrib.auth.views import *
from django.contrib.auth.forms import *
import login

urlpatterns = patterns('',
    url(r'^notverified/$', not_verified, name='not_verified'),
    url(r'^reset/$', 'login.views.reset', name='reset'),
    url(r'^login/$', 'login.views.login',{'template_name': 'registration/log.html'},name='login'),
    url(r'^logout/$', logout_page,name='logout'),
    url(r'^register/$', register,name='register'),
    url(r'^profile/$', register_profile,name='profile'),
    url(r'^editprofile/$', edit_profile,name='editprofile'),
    url(r'^confirm/(?P<activation_key>\w+)/$',confirm,name='confirm'),
    url(r'^display/$',display,name='display'),
    url(r'^reset/done/$','django.contrib.auth.views.password_reset_done',{'template_name':'registration/password_reset_done.html'}, name='password_reset_done'),	 
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$','login.views.reset_confirm',name='password_reset_confirm'),
)
