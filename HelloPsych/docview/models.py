from django.db import models
from login.models import doctor, patient
from django.conf import settings
from django.contrib.auth.models import User

class request_call(models.Model):
    dts = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(patient)
    doc = models.ForeignKey(doctor)
    date_booked = models.DateField()
    start_tim = models.TimeField(default="12:00:00")
    end_tim = models.TimeField(default="12:15:00")
    sent = models.BooleanField(default=False)
    acknowledged = models.BooleanField(default=False)
    doctor_comments = models.CharField(max_length=200, blank=True, default="")
    calldone = models.BooleanField(default=False)
    callpending = models.BooleanField(default=True)
    callinprogress = models.BooleanField(default=False)
    prescription_sent = models.BooleanField(default=False)
    def __unicode__(self):
        return u'%s requested call for doctor %s for the date %s' % \
        (self.patient.username, self.doc.username, self.date_booked)

class timeslot(models.Model):
    doc = models.ForeignKey(doctor)
    weekday = (
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    )
    day = models.CharField(max_length=20, choices=weekday)
    start_time = models.TimeField()
    end_time = models.TimeField()
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        if self.enabled is True:
            return u'Doctor %s is available on %s from %s to %s' % \
            (self.doc, self.day, self.start_time, self.end_time)
        else:
            return u'Doctor %s is unavailable on %s from %s to %s' % \
            (self.doc, self.day, self.start_time, self.end_time)

class specializations(models.Model):
    doc = models.ForeignKey(doctor, to_field='username')
    specialization = (
         ('Addiction', 'Addiction'),
         ('Depression', 'Depression'),
         ('Fear', 'Phobias'),
         ('Relationship', 'Relationship'),
         ('Life', 'Life'),
         ('Hallucination', 'Hallucination'),
         ('Education', 'Education'),
         ('Anon', 'Others'),
    )
    expertise = models.CharField(max_length=200, choices=settings.SPECIALIZATION)
    def __unicode__(self):
        return u'Dr. %s %s specializes in %s' % \
        (self.doc.first_name, self.doc.last_name, self.expertise)


class job(models.Model):
    doc = models.ForeignKey(doctor)
    title = models.CharField(max_length=30)
    organization = models.CharField(max_length=30)
    description = models.TextField()
    def __unicode__(self):
        return self.title

class reschedule_request(models.Model):
    dts = models.DateTimeField(auto_now_add=True)
    request_from = models.ForeignKey(User, related_name='request_from')
    requested_to = models.ForeignKey(User, related_name='requested_to')
    date_booked = models.DateField()
    start_tim = models.TimeField(default="12:00:00")
    end_tim = models.TimeField(default="12:15:00")    
