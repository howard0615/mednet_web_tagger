from django import forms
from .models import Question
from django.contrib.auth.models import User

class summaryQuestionForm(forms.ModelForm):
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

class summaryUserDetailForm(forms.Form):
    question = forms.ModelChoiceField(queryset=Question.objects.all())
    Time_stamp = forms.DateTimeInput()
    sUser = forms.ModelChoiceField(queryset=User.objects.all())