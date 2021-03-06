from django.conf.urls import url
from django.contrib.auth import logout
from . import views


urlpatterns = [
    url(r'social/login/$', views.login, name='social_login'),
    url(r'profile/$', views.profile, name='profile'),
    url(r'logout/$', logout, name='logout'),
    url(r'ocrdata/$', views.get_ocr_data, name='get_ocr_data'),
    url(r'rank/$', views.rank_user, name='rank_user'),
    url(r'latest_orcdata', views.get_lastest_ocr, name='get_lastest_orc_data')
]
