from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from jeevesdb.JeevesModel import JeevesModel as Model, JeevesForeignKey as ForeignKey
from jeevesdb.JeevesModel import label_for

from sourcetrans.macro_module import macros, jeeves
import JeevesLib

# Create your models here.
class Department(Model):
    dept_name = models.CharField(max_length = 128)

class Employee(User):
    department = ForeignKey(Department, on_delete=models.CASCADE)

class Project(Model):
    project_name = models.CharField(max_length = 128)
    start_date = models.DateTimeField('date started')
    end_date = models.DateTimeField('date ended')
    department = ForeignKey(Department, on_delete=models.CASCADE)

    @staticmethod
    def get_jeeves_private_project_name(project):
        return "[redacted]"

    @staticmethod
    @label_for('project_name')
    @jeeves
    def jeeves_restrict_projectlabel(project, ctxt):
        return project.department == ctxt.department
