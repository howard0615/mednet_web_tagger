from django.db import models
from django.conf import settings
from labeltask.models import SetLabelTask
from question.models import Question
# Create your models here.

class Label(models.Model):
    LUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    LLabel_task = models.ForeignKey(SetLabelTask, on_delete=models.CASCADE)
    LAdequacy = models.IntegerField(help_text="0, 1", null=True)
    LDeducibility = models.IntegerField(help_text="0, 1", null=True)
    LAbstractive = models.IntegerField(help_text="0, 1", null=True)
    LNote = models.CharField(blank=True,help_text="備註", max_length=30, null=True)

    def __str__(self):
        return "{} {}".format(self.LUser.username, self.LLabel_task.tQuestion, self.LLabel_task.tdone)