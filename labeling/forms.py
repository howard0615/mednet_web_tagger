from dataclasses import field
from django import forms
from .models import Label
from question.models import Question

class labelQuestionForm(forms.ModelForm):
    # LUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # LLabel_task = models.ForeignKey(SetLabelTask, on_delete=models.CASCADE)
    # LAdequacy = models.IntegerField(help_text="0, 1")
    # LDeducibility = models.IntegerField(help_text="0, 1")
    # LAbstractive = models.IntegerField(help_text="0, 1")
    # LNote = models.CharField(help_text="備註", max_length=30)
    class Meta:
        model = Label
        fields = ['LAdequacy', 'LDeducibility', 'LAbstractive', 'LNote']
        labels = {
            'LAdequacy': '充分性',
            'LDeducibility': '可演繹性',
            'LAbstractive': '抽象性',
            'LNote': '備註'
        }
        widgets = {
            "LAdequacy": forms.NumberInput(attrs={'class': 'form-control'}),
            "LDeducibility": forms.NumberInput(attrs={'class': 'form-control'}),
            "LAbstractive": forms.NumberInput(attrs={'class': 'form-control'}),
            'LNote': forms.Textarea(attrs={'class': 'form-control', 'style':'height:50px;'}),
        }

class ReviewQuestionForm(forms.ModelForm):
    # fOriginal_Question = forms.CharField()
    # fQuery = forms.CharField()
    # fQuestion_Type = forms.IntegerField()
    class Meta:
        model = Question
        fields = ['qOriginal_Question', 'sQuery', 'sQuestion_Type']
        labels = {
            'qOriginal_Question': ('原始問題'),
            'sQuery': ('摘要問題'),
            'sQuestion_Type': ('問題種類')
        }
        widgets = {
            'qOriginal_Question': forms.Textarea(attrs={'class': 'form-control', 'style':'height:150px;'}),
            'sQuery': forms.Textarea(attrs={'class': 'form-control', 'style':'height:100px;' , 'placeholder': '對原始問題摘要，並對其問題分類'}),
            'sQuestion_Type': forms.Select(attrs={'class': 'form-control'}),
        }