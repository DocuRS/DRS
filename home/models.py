from __future__ import unicode_literals

import datetime
from enum import Enum

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from jeevesdb.JeevesModel import JeevesModel as Model, JeevesForeignKey as ForeignKey
from jeevesdb.JeevesModel import label_for

import os
from sourcetrans.macro_module import macros, jeeves
import JeevesLib

class Levels(Enum):
    PUBLIC = 0
    CONFIDENTIAL = 1
    SECRET = 2
    TOP_SECRET = 3

# Create your models here.
class Department(Model):
    dept_name = models.CharField(max_length = 128)


class UserProfile(Model):
    username = models.CharField(max_length=1024)
    email = models.CharField(max_length=1024)
    name = models.CharField(max_length=1024)
    clearance = models.IntegerField(default=Levels.PUBLIC)
    department = ForeignKey(Department, on_delete=models.CASCADE)
    #role =  'admin'

    @staticmethod
    def jeeves_get_private_email(user):
        return "[redacted]"

    @staticmethod
    @label_for('email')
    @jeeves
    def jeeves_restrict_userprofilelabel(user, ctxt):
        return user == ctxt

class Project(Model):
    project_name = models.CharField(max_length = 128)
    code_name = models.CharField(max_length = 128)
    start_date = models.DateTimeField('date started')
    end_date = models.DateTimeField('date ended')
    department = ForeignKey(Department, on_delete=models.CASCADE)
    #url = "/project?id=" + self.jeeves_id

    @staticmethod
    def jeeves_get_private_project_name(project):
        return project.code_name

    @staticmethod
    @label_for('project_name')
    @jeeves
    def jeeves_restrict_projectlabel(project, ctxt):
        return project.department == ctxt.department

    def __str__(self):
        return self.project_name

class Document(Model):
    document_name = models.CharField(max_length = 128)
    description = models.CharField(max_length = 512)
    last_accessed_by = ForeignKey(UserProfile, on_delete=models.CASCADE)
    department = ForeignKey(Department, on_delete=models.CASCADE)
    classification = models.IntegerField(default=Levels.TOP_SECRET)
    project = ForeignKey(Project, on_delete=models.CASCADE)
    filedata = models.FileField(upload_to='rep/')

    @staticmethod
    def jeeves_get_private_document_name(document):
        return "[redacted]"

    @staticmethod
    @label_for('document_name')
    @jeeves
    def jeeves_restrict_documentlabel(document, ctxt):
        return document.classification <= ctxt.clearance and document.department == ctxt.department

    def __str__(self):
        return "%s:%s" % (self.document_name,self.classification)

from django.dispatch import receiver
from django.db.models.signals import post_syncdb
import sys
current_module = sys.modules[__name__]
@receiver(post_syncdb, sender=current_module)
def dbSynced(sender, **kwargs):
    if settings.DEBUG:
        execfile(os.path.join(settings.BASE_DIR, 'SampleData.py'))
