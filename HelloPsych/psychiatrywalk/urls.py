from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'psychiatrywalk.views.home'),
     url(r'^home/$',include('patientview.urls')),	
     url(r'^welcome/',include('patientview.urls',namespace='patient')),
     url(r'^accounts/login/', include('login.urls',namespace='login')),
     url(r'^call/(?P<reciever>\w+)/(?P<req_id>\d+)/',include('vline.urls',namespace='vline')),
     url(r'^icall/(?P<reciever>\w+)/(?P<req_id>\d+)/','vline.views.broad'),
     url(r'^getp/$','patientview.views.get'),
     url(r'^creds/$','vline.views.update_credits'),
     url(r'^update_comments/$','vline.views.update_comments'),
     url(r'^get/$','docview.views.get'),
     url(r'^getb/$','patientview.views.iget'),
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     url(r'^dr/',include('docview.urls',namespace='docview')),
     url(r'^presc/',include('prescription.urls',namespace='prescription')),
     url(r'^login/', include('login.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^cal/(?P<doc_id>\d+)/','docview.views.calendar'),
     url(r'^notify/$','patientview.views.notify'),
     url(r'^message/',include('messageapp.urls',namespace='messageapp')),   
)

    #url(r'^vline/$', include('vline.urls')),
     #url(r'^i18n/',include('django.conf.urls.i18n')),
     #url(r'^login/$','psyche.views.login_user'),
     #url(r'^post/$','psyche.views.post'),
