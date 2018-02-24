from django.db import models

# Create your models here.

'''
TimeStamp

created_at DateTimeField 생성시간
update_at DateTimeField 생성시간

'''


class TimeStamp(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
