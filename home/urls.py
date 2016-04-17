from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^register/$', views.register_account),
    url(r'^index/$', views.landing),
    url(r'^$', views.landing),
]
