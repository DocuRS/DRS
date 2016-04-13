from .models import Project, UserProfile, Department
from datetime import datetime
from django.contrib.auth.models import User

cs = Department.objects.create(dept_name = "Computer Science")
ee = Department.objects.create(dept_name = "Electrical Engineering")

kushalUser=UserProfile.objects.create(
    username="kushal"
  , email="kushal@sjsu.edu"
  , name="Kushal Palesha"
  , department=cs)
User.objects.create_user('kushal', 'kushal@sjsu.edu', 'kushal')
dhruvenUser=UserProfile.objects.create(
    username="dhruven"
  , email="dhruven@sjsu.edu"
  , name="Dhruven Vora"
  , department=cs)
User.objects.create_user('dhruven', 'dhruven@sjsu.edu', 'dhruven')

Project.objects.create(project_name = "Document Repository System", start_date = datetime.now(), end_date = datetime.now(), department = cs)

Project.objects.create(project_name = "Video Server", start_date = datetime.now(), end_date = datetime.now(), department = ee)
