from django.conf.urls import url
from django.contrib.auth import logout
from . import views


urlpatterns = [
    url(r'social/login/$', views.login, name='social_login'),
    url(r'profile/$', views.profile, name='profile'),
    url(r'logout/$', logout, name='logout'),
]