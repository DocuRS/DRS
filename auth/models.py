from __future__ import unicode_literals

from django.db import models

# Create your models here.
"""
This class stores the user authentication details such as username and password.
"""
class UserAuth(models.Model):
    userid = models.CharField(max_length = 16, primary_key=True) #primary key
	password = models.CharField(max_length = 100)

	def __str__(self):
		return self.userid

"""
This class stores the details of the user.
"""		
class User(models.Model):
    userid = models.CharField(max_length = 16, primary_key=True) #primary key
	name = models.CharField(max_length = 100)
	dept_id = models.CharField(max_length = 8)

	def __str__(self):
		return self.name