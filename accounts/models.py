from django.db import models
from django.conf import settings
from core.models import TimeStamp
# Create your models here.


'''
Profile

name 유저이름 CharField
email 유저 이메일 EmailField
phone 연락처 CharField 
EyeInfo 눈 건강정보 foreignkey
ocr_am 오전 ocr floatfield
ocr_pm 오후 ocr floatfield
ocr_now 최신 ocr floatfield
ocr_yesterady 어제 ocr floatfield
ocr_month 이번달 평균 ocr floatfield
'''


class Profile(TimeStamp):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=128, blank=False, null=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=128)
    ocr_am = models.FloatField(default=0.0)
    ocr_pm = models.FloatField(default=0.0)
    ocr_now = models.FloatField(default=0.0)
    ocr_yesterday = models.FloatField(default=0.0)
    ocr_month = models.FloatField(default=0.0)
