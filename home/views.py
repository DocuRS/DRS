from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from .models import Project

from sourcetrans.macro_module import macros, jeeves
import JeevesLib
#from django.contrib.auth.models import User

#warning: HttpResponseRedirect does not work in dJango 1.6.5
# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def login(request):
    userid = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=userid, password=password)
    if user is not None:
        # the password verified for the user
        if user.is_active:
            project_list = Project.objects.all()
            return render(request, "home/landing.html", {'project_list': project_list})
        else:
            # the authentication system was unable to verify the username and password
            return render(request, "home/index.html", {
                'error_message': "User is not active"
            })
    else:
        # the authentication system was unable to verify the username and password
        return render(request, "home/index.html", {
            'error_message': "Invalid User"
        })

def landing(request):
    return render(request, "home/landing.html")
