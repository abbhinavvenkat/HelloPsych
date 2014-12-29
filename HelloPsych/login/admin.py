from django.contrib import admin
from login.models import *
from patientview.models import *

admin.site.register(patient)
admin.site.register(doctor)
admin.site.register(UserProfile)
admin.site.register(profileupdate)


