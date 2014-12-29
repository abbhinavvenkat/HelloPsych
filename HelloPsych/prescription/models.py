from django.db import models
from django.forms import ModelForm
from login.models import doctor, patient
from docview.models import request_call

class generic(models.Model):
    name = models.TextField(max_length=500, default="", null=False)
    def __unicode__(self):
        return self.name

class brand(models.Model):
    name = models.TextField(max_length=500, default="", null=False)
    qty = models.IntegerField(default=100)
    unit = models.TextField(max_length=50, default="", null=False)
    category = models.ForeignKey(generic)
    def __unicode__(self):
        return u'%s:%d %s' % (self.name, self.qty, self.unit)

class dosage(models.Model):
    generic = models.ForeignKey(generic)
    frequency = models.TextField(default="", null=False)
    comment = models.TextField(default="", blank=True, null=True)
    duration = models.TextField(default="", blank=False, null=False)
    def __unicode__(self):
        return u'%s: %s' % (self.generic.name, self.frequency)

class prescription(models.Model):
    dts = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(patient, related_name="presc_pat")
    doc = models.ForeignKey(doctor, related_name="presc_doc")
    medicines = models.ManyToManyField(dosage, blank=True, \
        null=True)
    appointment = models.ForeignKey(request_call, related_name="prescribed_for")
    concern = models.TextField(max_length=280)
    symptoms = models.TextField(default="", null=False)
    doctor_comments = models.TextField(default="NULL",blank=True, max_length=200)
    def __unicode__(self):
        return u'Appointment No.: %s for Dr. %s %s booked by \
            patient %s %s' % (self.appointment.id, \
            self.doc.first_name, self.doc.last_name, \
            self.patient.first_name, self.patient.last_name)
     
class PrescriptionForm(ModelForm):
    class Meta:
        model = prescription
  
    def __init__(self):
        count = kwargs.get('count', 1)
        super(PrescriptionForm, self).__init__(*args, **kwargs)
        for i in range(count):
            self.fields['dosage_%s' % i]=forms.CharField(label="Generic")
            self.fields['brand_%s' % i]=forms.CharField(label="Brand")
            self.fields['freq_%s' % i]=forms.CharField(label="Frequency")

