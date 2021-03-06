from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from .models import Project, UserProfile, Department, Document, Levels
from datetime import datetime
import cgi
from django.db import transaction

from sourcetrans.macro_module import macros, jeeves
import JeevesLib
#from django.contrib.auth.models import User

# Create your views here.

@jeeves
def add_to_context(context_dict, request, template_name, profile, concretize):
    template_name = concretize(template_name)
    context_dict['concretize'] = concretize

    context_dict['is_admin'] = profile != None and profile.level == "chair"
    context_dict['profile'] = profile

    context_dict['is_logged_in'] = (request.user and
                                    request.user.is_authenticated() and
                                    (not request.user.is_anonymous()))

'''
Wraps around a request by getting the user and defining functions like
concretize.
'''
def request_wrapper(view_fn, *args, **kwargs):
    def real_view_fn(request):
        try:
            profile = UserProfile.objects.get(username=request.user.username)
            ans = view_fn(request, profile, *args, **kwargs)
            template_name = ans[0]
            context_dict = ans[1]

            if template_name == "redirect":
                path = context_dict
                return HttpResponseRedirect(JeevesLib.concretize(profile, path))

            concretizeState = JeevesLib.jeevesState.policyenv.getNewSolverState(profile)
            def concretize(val):
                return concretizeState.concretizeExp(val, JeevesLib.jeevesState.pathenv.getEnv())
            add_to_context(context_dict, request, template_name, profile, concretize)

            return render_to_response(template_name, RequestContext(request, context_dict))

        except Exception:
            import traceback
            traceback.print_exc()
            raise
        finally:
            # Clear concretization cache.
            JeevesLib.clear_cache()

    real_view_fn.__name__ = view_fn.__name__
    return real_view_fn

def register_account(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("index")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()

            User.objects.create(
                username=user.username
              , email=request.POST.get('email', '')
              , name=request.POST.get('name', '')
            )

            user = authenticate(username=request.POST['username'],
                         password=request.POST['password1'])
            login(request, user)
            return HttpResponseRedirect("index")
    else:
        form = UserCreationForm()

    return render_to_response("registration/account.html", RequestContext(request,
        {
            'form' : form,
            'which_page' : "register"
        }))

# def login(request):
#     userid = request.POST['username']
#     password = request.POST['password']
#     print userid
#     user = authenticate(username=userid, password=password)
#     if user is not None:
#         # the password verified for the user
#         if user.is_active:
#             project_list = Project.objects.all()
#             return render(request, "home/landing.html", {'project_list': project_list})
#         else:
#             # the authentication system was unable to verify the username and password
#             return render(request, "home/index.html", {
#                 'error_message': "User is not active"
#             })
#     else:
#         # the authentication system was unable to verify the username and password
#         return render(request, "home/index.html", {
#             'error_message': "Invalid User"
#         })

@login_required
@request_wrapper
@jeeves
def landing(request, user_profile):
    JeevesLib.set_viewer(user_profile)
    projects = Project.objects.all()
    return ("landing.html", { 'projects': projects, 'which_page': "landing" })

@login_required
@request_wrapper
@jeeves
def project_home(request, user_profile):
    JeevesLib.set_viewer(user_profile)
    project = Project.objects.get(jeeves_id=request.GET.get('id'))
    documents = Document.objects.filter(project=project).all()
    return ("project_home.html", {'documents': documents, 'which_page': "project_home", 'project_name': project.project_name, 'project_id': request.GET.get('id')})

@login_required
@request_wrapper
@jeeves
def add_project(request, user_profile):
    JeevesLib.set_viewer(user_profile)
    dept_name = user_profile.department.dept_name
    return ("add_project.html", {'dept_name': dept_name,})

@login_required
@request_wrapper
@jeeves
def add_new_project(request, user_profile):
    JeevesLib.set_viewer(user_profile)
    project_name = request.POST['project_name']
    code_name = request.POST['code_name']
    department = Department.objects.get(dept_name=request.POST['dept_name'])
    Project.objects.create(
        project_name = project_name,
        code_name = code_name,
        start_date = datetime.now(),
        end_date = datetime.now(),
        department = department)
    #TODO: redirect to the landing page.
    return ("add_project.html", {'dept_name': department.dept_name})

@login_required
@request_wrapper
@jeeves
def add_document(request, user_profile):
    JeevesLib.set_viewer(user_profile)
    project_id = request.GET["p"];
    return ("add_document.html", {'project_id': project_id})

@login_required
@request_wrapper
@jeeves
@transaction.commit_on_success
def add_new_document(request, user_profile):
    JeevesLib.set_viewer(user_profile)

    document_name = request.POST.get('document_name')
    description = request.POST.get('description')
    classification = request.POST.get('classification')
    project_id = request.POST.get('project_id')
    filedata = request.FILES.get('docfile')
    department = user_profile.department

    project = Project.objects.get(jeeves_id=project_id)

    #If we don't concretize the filedata, DRS will store the file twice.
    filedata = JeevesLib.concretize(user_profile, filedata)

    Document.objects.create(
        document_name = document_name,
        description = description,
        last_accessed_by = user_profile,
        department = department,
        classification = getattr(Levels, classification),
        project = project,
        filedata = filedata)

    return ("add_document.html", {'project_id': project_id})


def getAllDocuments(project):
    return Document.objects.filter(project=project).all()
