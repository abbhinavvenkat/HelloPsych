from django.db import models
from django.contrib.auth.models import User

class patient(models.Model):
	user=models.OneToOneField(User)
	first_name=models.CharField(max_length=50)
	last_name=models.CharField(max_length=50)
	marital_status=(
			('S','Single'),
			('M','Married'),
			('D','Divorced'),
		       )

class doctor(models.Model):
	user=models.OneToOneField(User)
	first_name=models.CharField(max_length=50)
	last_name=models.CharField(max_length=50)
	expertise=models.CharField(max_length=200)


class logs(models.Model):
	user=models.OneToOneField(User)
	login_time=models.DateTimeField()
    
# Create your models here.
