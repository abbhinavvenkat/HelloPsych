from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class UserProfile(models.Model):
    '''Extending the User class'''
    user = models.ForeignKey(User, to_field = 'id')
    acc_type = models.BooleanField()
    activation_key = models.CharField(max_length = 257)
    key_expires = models.DateTimeField()
    verified = models.BooleanField()

class patient(models.Model):
    '''Patient model'''  
    user = models.OneToOneField(User)
    username = models.CharField(max_length = 50, unique = True)
    first_name = models.CharField(max_length = 50, default = "FirstName")
    last_name = models.CharField(max_length = 50, default = "LastName")
    propic = models.ImageField(upload_to = 'static/propics')
    age = models.IntegerField()
    SEX_CHOICES = (
        ('M','Male'),
        ('F','Female'),
    )
    sex = models.CharField(max_length = 1, choices = SEX_CHOICES)
    concern = models.CharField(max_length = 20, choices = settings.SPECIALIZATION, default = "NULL")
    MARITAL_CHOICES = (
        ('S','Single'),
        ('M','Married'),
        ('D','Divorced'),
    )
    marital_status = models.CharField(max_length = 1, choices = MARITAL_CHOICES)
    first_call = models.BooleanField(default = False)
    credits = models.IntegerField(default = 20)

class profileupdate(models.Model):
    user = models.OneToOneField(User)

class doctor(models.Model):
    '''Doctor model'''
    user = models.OneToOneField(User)
    username = models.CharField(unique = True, max_length = 50)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    propic = models.ImageField(upload_to = 'static/propics', default = 'static/propics/a.jpg')
    address = models.TextField(null = True, blank = True)
    phone_no = models.BigIntegerField(blank = True)
    location = models.CharField(null = True, max_length = 50, blank = True)
    current_job = models.TextField(null = True, blank = True)
    memberships = models.TextField(null = True, blank = True)
    projects = models.TextField(null = True, blank = True)
    prev_exp = models.TextField(null = True, blank = True)
    description = models.TextField(null = True, blank = True)
    ug_degree = models.CharField(max_length = 50)
    ug_council = models.CharField(max_length = 50)
    ug_college = models.CharField(max_length = 50)
    ug_year = models.IntegerField()
    ug_regno = models.BigIntegerField()
    pg_degree = models.CharField(max_length = 50)
    pg_college = models.CharField(max_length = 50)
    pg_regno = models.BigIntegerField(max_length = 50)
    pg_council = models.CharField(max_length = 50)
    pg_year = models.IntegerField()
    credits = models.IntegerField(default=0)
    consultation_fee = models.IntegerField(default = 9)
    others = models.TextField(null = True, blank=True)
    pref_time = models.TimeField(blank = True, null=True)
    expertise = models.CharField(max_length = 200, choices = settings.SPECIALIZATION)
    
    def __unicode__(self):
        return u'%s' % (self.username)
    
class logs(models.Model):
    user = models.OneToOneField(User)
    login_time = models.DateTimeField()


