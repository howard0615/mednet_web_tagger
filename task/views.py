from venv import create
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from task.models import SetTask
from question.models import Question
from .forms import distribute_task_form
# Create your views here.

@login_required
def task_situations(request):
    Users_model = get_user_model() # 現有的users
    users = Users_model.objects.all()
    total_task = SetTask.objects.values('tStartTime').distinct()
    Task = {}
    for date_qs in total_task:
        date_time = date_qs['tStartTime']
        date_time_value = date_time.strftime("%Y/%m/%d")
        same_date_data = SetTask.objects.filter(tStartTime=date_time)
        users = same_date_data.values('tUser').distinct()
        date_data = {}
        for user in users:
            user_name = Users_model.objects.get(pk=user['tUser'])
            print(user_name.username)
            user_qs = same_date_data.filter(tUser = Users_model.objects.get(pk=user['tUser']))
            total_data_num = user_qs.count()
            done_data_num = user_qs.filter(tdone = True).count()
            user_date = {'done_data_num': done_data_num, 'total_data_num': total_data_num}
            #save in dict
            date_data[user_name.username] = user_date
        Task[date_time_value] = date_data

            
    context = {
        'Task': Task
    }

    return render(request, 'task/task_situations.html', context)

 
@login_required
def distribute_task(request):
    task_form = distribute_task_form(request.POST or None)
    context = {
        'task_form': task_form,
        'alert': False,
        'alert_msg': '',
        'success': False,
        'success_msg': ''
    }

    current_users = get_user_model()
    users = current_users.objects.all()
    user_choices = {user.id: user.username for user in users}
    if request.method == "POST":
        if task_form.is_valid():
            form_data = task_form.cleaned_data
            
            q = Question.objects.filter(sQuestion_Filter=0).exclude(settask__tdone=False).exclude(settask__tdone=True).order_by('qQuestion_ID')
            success_num = 0

            for num in range(form_data['task_data_number']):
                try:
                    set_task = SetTask.objects.create(tUser = current_users.objects.get(pk=form_data['User_name']), 
                                                    tQuestion = q[num],
                                                    tStartTime = form_data['date'],
                                                    tdone = False)
                
                    set_task.save()
                    success_num += 1
                    context['success']=True
                except IndexError:
                    context['alert']= True
                    context['alert_msg'] = "資料庫已沒有可分派的資料"
            context['success_msg'] = "成功分派給 {} 在 {} 共 {}份".format(current_users.objects.get(pk=form_data['User_name']), form_data['date'], success_num)
        
    return render(request, 'task/distribute_task.html', context)