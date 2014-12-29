from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from login.models import *

class message(models.Model):
    sender = models.ForeignKey(User, related_name='creator')
    receiver = models.ForeignKey(User, related_name='assignee')
    dts = models.DateTimeField(default=datetime.now)
    subject = models.TextField()
    text_message = models.TextField()
