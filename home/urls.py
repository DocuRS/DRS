from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^register/$', views.register_account),
    url(r'^project/new/$', views.add_project),
    url(r'^project/add/$', views.add_new_project),
    url(r'^project/upload/new$', views.add_new_document),
    url(r'^project/upload/$', views.add_document),
    url(r'^project/$', views.project_home),
    url(r'^index/$', views.landing),
    url(r'^$', views.landing),
]
