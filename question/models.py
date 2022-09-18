from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Question(models.Model):
    qQuestion_ID = models.IntegerField(primary_key=True, unique=True)
    qQuestion_Title = models.CharField(max_length=100)
    qOriginal_Question = models.TextField(max_length=1000)
    QUES_TYPE_CHOICES = (
        (0, '未選擇 NOT selected'),
        (1, '病症 symptoms'),
        (2, '藥物 drugs'),
        (3, '科室 department'),
        (4, '治療 treatment'),
        (5, '檢查 examination'),
        (6, '資訊 informantion'),
        (7, '再討論...')
    )
    QUES_FILTER = (
        (0, "Haven't filter"),
        (1, 'Single'),
        (2, 'Single & Often'),
        (3, 'Multi'),
        (4, 'Discuss'),
        (5, 'Trash')
    )
    sQuery = models.TextField(
        max_length=500, null=True, blank=True, default=None)
    sQuestion_Type = models.PositiveSmallIntegerField(
        null=True, choices=QUES_TYPE_CHOICES, default=None)
    sQuestion_Filter = models.PositiveSmallIntegerField(
        null=True, choices=QUES_FILTER, default=None)

    def __str__(self):
        return 'id: {}'.format(self.qQuestion_ID)



class Summarization(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    Time_stamp = models.TimeField(default=timezone.now)
    sUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "summarization: id{}".format(self.question.qQuestion_ID)


# class WhoIsGoingToSum(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     WUser = models.ForeignKey(settings.A, on_delete=models.SET_NULL, null=True)