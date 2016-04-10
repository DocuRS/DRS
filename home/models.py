from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    dept_name = models.CharField(max_length = 128)

    def __str__(self):
        return self.dept_name

class Employee(User):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name
        
class Project(models.Model):
    project_name = models.CharField(max_length = 128)
    start_date = models.DateTimeField('date started')
    end_date = models.DateTimeField('date ended')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.project_name
