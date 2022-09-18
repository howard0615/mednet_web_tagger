from django.db import models
from django.utils import timezone
from question.models import Question
from django.conf import settings

# Create your models here.

class SetTask(models.Model):
    tUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tQuestion = models.ForeignKey(Question, on_delete=models.CASCADE)
    tStartTime = models.DateField(default=timezone.now)
    tdone = models.BooleanField(default=False)

    def __str__(self):
        return "{}, {}".format(self.tUser.username, self.tQuestion)