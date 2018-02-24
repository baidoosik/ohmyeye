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
    # 오전
    ocr_am = models.FloatField(default=0.0)
    ocr_am_count = models.IntegerField(default=0)
    ocr_am_total = models.FloatField(default=0)
    # 오후
    ocr_pm = models.FloatField(default=0.0)
    ocr_pm_count = models.IntegerField(default=0)
    ocr_pm_total = models.FloatField(default=0)
    # 현재
    ocr_now = models.FloatField(default=0.0)
    # 어제
    ocr_yesterday = models.FloatField(default=0.0)
    ocr_yesterday_count = models.IntegerField(default=0)
    ocr_yesterday_total = models.FloatField(default=0)
    # 이번 달
    ocr_month = models.FloatField(default=0.0)
    ocr_month_count = models.IntegerField(default=0)
    ocr_month_total = models.FloatField(default=0.0)

    def __str__(self):
        return self.name + '프로필'

    def calculate_ocr_am(self, time):
        ocr = (10/time)*10/16.6*100
        self.ocr_now = ocr
        # 오전
        self.ocr_am_total += ocr
        self.ocr_am_count += 1
        self.ocr_am = (self.ocr_am_total)/self.ocr_am_count
        self.save()

    def calculate_ocr_pm(self, time):
        ocr = (10/time)*10/16.6*100
        self.ocr_now = ocr
        # 오후
        self.ocr_pm_total += ocr
        self.ocr_pm_count += 1
        self.ocr_pm = (self.ocr_pm_total)/self.ocr_pm_count
        self.save()

    @staticmethod
    def one_day_ocr_data_batch():
        for profile in Profile.objects.all():
            # yesterday로 데이터 이전
            profile.ocr_yesterday = (profile.ocr_am_total + profile.ocr_pm_total)\
                                    / (profile.ocr_am_count+profile.ocr_pm_count)
            profile.ocr_yesterday_total = profile.ocr_am_total + profile.ocr_pm_total
            Profile.ocr_yesterday_count = profile.ocr_am_count+profile.ocr_pm_count

            # 오전 오후 데이터 초기화
            profile.ocr_am_count = 0
            profile.ocr_am_total = 0.0
            profile.ocr_pm_count = 0
            profile.ocr_pm_total = 0.0

            # yesterday 데이터 한 달 데이터로 이전
            profile.ocr_month_count += profile.ocr_yesterday_count
            profile.ocr_month_total += profile.ocr_yesterday_total
            profile.ocr_month = profile.ocr_month_total / profile.ocr_month_total

            profile.save()

    @staticmethod
    def one_month_data_batch():
        for profile in Profile.objects.all():
            profile.ocr_month_total = 0.0
            profile.ocr_month_count = 0
            profile.ocr_month = 0.0

            profile.save()