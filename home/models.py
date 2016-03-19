from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserActivity(models.Model):
    userid = models.CharField(max_length = 16, primary_key=True) #primary key
    login_time = models.CharField(max_length = 100)
