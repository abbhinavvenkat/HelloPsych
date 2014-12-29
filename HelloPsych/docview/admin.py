from django.contrib import admin
from docview.models import request_call,  \
      timeslot, specializations, reschedule_request


admin.site.register(request_call)
admin.site.register(specializations)
#admin.site.register(job)
admin.site.register(timeslot)
admin.site.register(reschedule_request)
