from __future__ import unicode_literals

from django.db import models

# Create your models here.
"""
This class maintains the details of the file stored in the repository.
"""
class Document(models.Model):
    file_id = models.CharField(max_length = 32, primary_key=True) #primary key
    file_name = models.CharField(max_length = 64)
    author = models.CharField(max_length = 64)
    dept_id = models.CharField(max_length = 8)
    classification_id = models.CharField(max_length = 8)
    
    def __str__(self):
		return self.file_name