from re import L
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from .models import SetLabelTask
from .forms import distribute_label_task_form
from question.models import Question
# Create your views here.

# Admin才有能力使用到這裡

@user_passes_test(lambda u: u.is_superuser)
def label_task_situations(request):
    Users_model = get_user_model() # 現有的users
    users = Users_model.objects.all()
    total_task = SetLabelTask.objects.values('tStartTime').distinct()
    Task = {}
    for date_qs in total_task:
        date_time = date_qs['tStartTime']
        date_time_value = date_time.strftime("%Y/%m/%d")
        same_date_data = SetLabelTask.objects.filter(tStartTime=date_time)
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

    return render(request, 'label_task/label_task_situations.html', context)

@user_passes_test(lambda u: u.is_superuser)
def distribute_label_task(request):
    label_task_form = distribute_label_task_form(request.POST or None)
    current_users = get_user_model()
    users = current_users.objects.all()
    user_choices = {user.id: user.username for user in users}

    context = {
        'label_task_form': label_task_form,
        'alert': False,
        'alert_msg': '',
        'success': False,
        'success_msg': ''
    }

    if request.method == "POST":
        if label_task_form.is_valid():
            form_data = label_task_form.cleaned_data
            
            #撈出已經摘要過的問題, 還沒被set label task
            q = Question.objects.exclude(sQuestion_Type=0).exclude(setlabeltask__tdone=False).exclude(setlabeltask__tdone=True).order_by('qQuestion_ID')
            success_num = 0
            for num in range(form_data['task_data_number']):
                qid = q[0].qQuestion_ID
                try:
                    for user in users.exclude(is_superuser=True):
                        print(q[num])
                        set_label_task = SetLabelTask.objects.create(tUser = user,
                                                                    tQuestion = Question.objects.get(qQuestion_ID=qid),
                                                                    tStartTime = form_data['date'],
                                                                    tdone = False)
                        set_label_task.save()
                        success_num += 1
                        context['success']=True
                except IndexError:
                    context['alert'] = True
                    context['alert_msg'] = "資料庫已沒有可分派的資料"
            context['success_msg'] = "成功分派給 {}位標記者在 {} 共 {}份".format(users.exclude(is_superuser=True).count(), form_data['date'], success_num)
    return render(request, 'label_task/distribute_label_task.html', context)