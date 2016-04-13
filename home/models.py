from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from jeevesdb.JeevesModel import JeevesModel as Model, JeevesForeignKey as ForeignKey
from jeevesdb.JeevesModel import label_for

import os
from sourcetrans.macro_module import macros, jeeves
import JeevesLib

# Create your models here.
class Department(Model):
    dept_name = models.CharField(max_length = 128)


class UserProfile(Model):
    username = models.CharField(max_length=1024)
    email = models.CharField(max_length=1024)
    name = models.CharField(max_length=1024)

    @staticmethod
    def jeeves_get_private_email(user):
        return "[redacted]"

    @staticmethod
    @label_for('email')
    @jeeves
    def jeeves_restrict_userprofilelabel(user, ctxt):
        return user == ctxt
    department = ForeignKey(Department, on_delete=models.CASCADE)


class Project(Model):
    project_name = models.CharField(max_length = 128)
    start_date = models.DateTimeField('date started')
    end_date = models.DateTimeField('date ended')
    department = ForeignKey(Department, on_delete=models.CASCADE)

    @staticmethod
    def jeeves_get_private_project_name(project):
        return "[redacted]"

    @staticmethod
    @label_for('project_name')
    @jeeves
    def jeeves_restrict_projectlabel(project, ctxt):
        return project.department == ctxt.department

from django.dispatch import receiver
from django.db.models.signals import post_syncdb
import sys
current_module = sys.modules[__name__]
@receiver(post_syncdb, sender=current_module)
def dbSynced(sender, **kwargs):
    if settings.DEBUG:
        execfile(os.path.join(settings.BASE_DIR, 'SampleData.py'))
