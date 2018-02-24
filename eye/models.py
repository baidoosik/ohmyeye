from django.db import models
from accounts.models import Profile
# Create your models here.


class EyeInfomation(models.Model):
    profile = models.ForeignKey(Profile)
    ibi_1 = models.FloatField(null=True, blank=True, default=0.0)
    ibi_2 = models.FloatField(null=True, blank=True, default=0.0)
    ibi_3 = models.FloatField(null=True, blank=True, default=0.0)
    ibi_4 = models.FloatField(null=True, blank=True, default=0.0)
    ibi_5 = models.FloatField(null=True, blank=True, default=0.0)
    ibi_6 = models.FloatField(null=True, blank=True, default=0.0)
    turn_num = models.IntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return self.profile.name + '최신 눈 데이터'

    def input_ibi_data(self, time):
        ibi = (time) / 10
        if self.turn_num == 1:
            self.ibi_1 = ibi
            self.turn_num += 1
        elif self.turn_num == 2:
            self.ibi_2 = ibi
            self.turn_num += 1
        elif self.turn_num == 3:
            self.ibi_3 = ibi
            self.turn_num += 1
        elif self.turn_num == 4:
            self.ibi_4 = ibi
            self.turn_num += 1
        elif self.turn_num == 5:
            self.ibi_5 = ibi
            self.turn_num += 1
        else:
            self.ibi_6 = ibi
            self.turn_num = 1
        self.save()

    def make_ibi_list(self):
        if self.turn_num == 1:
            result = [self.ibi_1, self.ibi_2, self.ibi_3, self.ibi_4, self.ibi_5, self.ibi_6]
        elif self.turn_num == 2:
            result = [self.ibi_2, self.ibi_3, self.ibi_4, self.ibi_5, self.ibi_6, self.ibi_1]
        elif self.turn_num == 3:
            result = [self.ibi_3, self.ibi_4, self.ibi_5, self.ibi_6, self.ibi_1, self.ibi_2]
        elif self.turn_num == 4:
            result = [self.ibi_4, self.ibi_5, self.ibi_6, self.ibi_1, self.ibi_2, self.ibi_3]
        elif self.turn_num == 5:
            result = [self.ibi_5, self.ibi_6, self.ibi_1, self.ibi_2, self.ibi_3, self.ibi_4]
        else:
            result = [self.ibi_6, self.ibi_1, self.ibi_2, self.ibi_3, self.ibi_4, self.ibi_5]
        return result
