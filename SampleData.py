from .models import Project, UserProfile, Department, Levels
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

projectJ = Project.objects.create(
    project_name = "Document Repository System",
    code_name = "Project_J",
    start_date = datetime.now(),
    end_date = datetime.now(),
    department = cs)

projectV = Project.objects.create(
    project_name = "Video Server",
    code_name = "Project_V",
    start_date = datetime.now(),
    end_date = datetime.now(),
    department = ee)

doc1 = Document.objects.create(
    document_name="Project_plan.docx",
    description="Project plan",
    last_accessed_by=kushalUser,
    department=cs,
    classification=Levels.SECRET,
    project=projectJ)

doc2 = Document.objects.create(
    document_name="Project_plan.docx",
    description="Project plan",
    last_accessed_by=dhruvenUser,
    department=ee,
    classification=Levels.SECRET,
    project=projectV)
