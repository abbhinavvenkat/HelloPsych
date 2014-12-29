from django.contrib import admin
from prescription.models import generic,  \
      brand, prescription, dosage

admin.site.register(generic)
admin.site.register(dosage)
admin.site.register(brand)
admin.site.register(prescription)
