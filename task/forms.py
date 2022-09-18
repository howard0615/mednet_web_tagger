import datetime
import django
from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

class distribute_task_form(forms.Form):
    try:
        current_users = get_user_model()
        users = current_users.objects.all()
        User_name = forms.ChoiceField(choices=((user.id, user.username) for user in users), widget=forms.Select(attrs={'class': 'form-control'}))
        task_data_number = forms.IntegerField(max_value=1000, widget = forms.NumberInput(attrs={'class': 'form-control'}))
        date = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget)
    except django.db.utils.OperationalError:
        pass
    except django.db.utils.ProgrammingError:
        pass