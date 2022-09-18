from tkinter import CASCADE
from django.db import models
from django.conf import settings
from question.models import Question
from django.utils import timezone

# Create your models here.


class SetLabelTask(models.Model):
    tUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tQuestion = models.ForeignKey(Question, on_delete=models.CASCADE)
    tStartTime = models.DateField(default=timezone.now)
    tdone = models.BooleanField(default=False)
    
    def __str__(self):
        return "{} {} {}".format(self.tUser.username, self.tQuestion, self.tdone)