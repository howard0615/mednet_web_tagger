
import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Summarization
from task.models import SetTask
from .forms import summaryQuestionForm
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Min, Max


# Create your views here.

@login_required
def your_questions_task(request):
    context = {}

    if request.user.is_authenticated:
        username = request.user.username
        user_id = request.user.id

    your_tasks = SetTask.objects.filter(tUser=user_id)
    #找出user中給予的task不同時間點 找出完是一個queryset
    # print(your_task.values('tStartTime').distinct())
    your_task_in_diff_dates = your_tasks.values('tStartTime').distinct()

    data_situation = {}
    for data_task in your_task_in_diff_dates:
        # print(datetime.date.today())
        # print(data_task['tStartTime'])
        if datetime.date.today() >= data_task['tStartTime']:
            d = SetTask.objects.filter(tStartTime = data_task['tStartTime'], tUser=user_id)
            undone = d.filter(tdone=True)
            data_situation[data_task['tStartTime'].strftime("%Y-%m-%d")] = undone.count()/d.count()*100
        else:
            pass
    context["data_situation"]=data_situation

    return render(request, 'questions/your_questions_task.html', context)

@login_required
def total_question_numbers(request):
    seen_questions_num = Question.objects.exclude(sQuestion_Filter=0).count()
    unseen_questions_num = Question.objects.filter(sQuestion_Filter=0).count()

    seen_per = round(seen_questions_num / (seen_questions_num + unseen_questions_num)*100, 1)
    unseen_per = round(unseen_questions_num / (seen_questions_num + unseen_questions_num)*100, 1)

    single_questions_num = Question.objects.filter(sQuestion_Filter=1).count()
    often_questions_num = Question.objects.filter(sQuestion_Filter=2).count()
    multi_questions_num = Question.objects.filter(sQuestion_Filter=3).count()
    discuss_questions_num = Question.objects.filter(sQuestion_Filter=4).count()
    trash_questions_num = Question.objects.filter(sQuestion_Filter=5).count()

    single_per = round(single_questions_num/seen_questions_num*100, 1)
    often_per = round(often_questions_num/seen_questions_num*100, 1)
    multi_per = round(multi_questions_num/seen_questions_num*100, 1)
    discuss_per = round(discuss_questions_num/seen_questions_num*100, 1)
    trash_per = round(trash_questions_num/seen_questions_num*100, 1)

    symptoms_type_num = Question.objects.filter(sQuestion_Type=1).count()
    drugs_type_num = Question.objects.filter(sQuestion_Type=2).count()
    department_type_num = Question.objects.filter(sQuestion_Type=3).count()
    treatment_type_num = Question.objects.filter(sQuestion_Type=4).count()
    examination_type_num = Question.objects.filter(sQuestion_Type=5).count()
    informantion_type_num = Question.objects.filter(sQuestion_Type=6).count()

    symptoms_per = round(symptoms_type_num/(single_questions_num+often_questions_num)*100, 1)
    drugs_per = round(drugs_type_num/(single_questions_num+often_questions_num)*100, 1)
    department_per = round(department_type_num/(single_questions_num+often_questions_num)*100, 1)
    treatment_per = round(treatment_type_num/(single_questions_num+often_questions_num)*100, 1)
    examination_per = round(examination_type_num/(single_questions_num+often_questions_num)*100, 1)
    information_per = round(informantion_type_num/(single_questions_num+often_questions_num)*100, 1)



    return render(request, 'questions/total_question_numbers.html', locals())

@login_required
def more_undo_id(request):
    med_undo_question_id_list = Question.objects.filter(sQuestion_Filter=0)
    undo_id_list = med_undo_question_id_list.values_list('qQuestion_ID', flat=True)

    context = {
        'undo_id_list': undo_id_list
    }
    return render(request, 'questions/more_undo_id.html', context)

@login_required
def question_view(request, ques_id):
    med_question_list = Question.objects.get(qQuestion_ID= ques_id)
    context = {
        'med_question_list': med_question_list
    }
    return render(request, 'questions/show.html', context)


@login_required
def date_rough_see(request, date):
    if request.method == 'POST':
        print(request.POST['summary_id'])
        return redirect(f'/questions/do_summary/{date}/{request.POST["summary_id"]}/')
    else:
        undone = Question.objects.filter(settask__tStartTime=date, settask__tUser=request.user.id, settask__tdone=False)
        done = Question.objects.filter(settask__tStartTime=date, settask__tUser=request.user.id, settask__tdone=True)
        context = {
            'undone': undone,
            'done': done
        }
    return render(request, 'questions/date_rough_see.html', context)


@login_required
def do_summary(request, date, ques_id):
    done_or_not = SetTask.objects.get(tQuestion=ques_id)
    med_question_list = Question.objects.get(qQuestion_ID= ques_id, settask__tStartTime=date, settask__tUser=request.user.id)
    summary_form = summaryQuestionForm(instance=med_question_list, 
                                        initial={'qOriginal_Question': med_question_list.qOriginal_Question,
                                                'sQuery': med_question_list.sQuery,
                                                'sQuestionType': med_question_list.sQuestion_Type})

    context = {'error': False, 'error_msg': '', 
                "summary_form": summary_form,
                'med_question_list': med_question_list, 
                'date': date,
                'done_or_not': done_or_not}

    #設一個model form 並將original question放入form中
    ques_filter_format = {'single': 1, 'often': 2, 'multi': 3, 'discuss': 4, 'trash': 5}

    
    if request.method == "POST": #如果是以POST方式才處理
        summary_form = summaryQuestionForm(request.POST, instance=med_question_list) #建立forms物件
        if summary_form.is_valid():  #通過forms驗證
            #med_question的資料
            Question_Filter = ques_filter_format[request.POST['ques_filter']]
            if Question_Filter == 1 or Question_Filter == 2:
                if summary_form.cleaned_data['sQuery'] == '':
                    context['summary_form'] = summary_form
                    context['error'] = True
                    context['error_msg'] = '請不要將『摘要問題』留白謝謝！！'
                    return render(request, 'questions/summary_ques_id.html', context)

                if summary_form.cleaned_data['sQuestion_Type'] == 0:
                    context['summary_form'] = summary_form
                    context['error'] = True
                    context['error_msg'] = '請選擇問題種類！！'
                    return render(request, 'questions/summary_ques_id.html', context)
                

            med_question_list.sQuestion_Filter = Question_Filter
            summary_form.save()
            med_question_list.save()

            #做這筆摘要的使用者資料
            user_id = request.user.id
            current_users = get_user_model()
            print(med_question_list)
            print(current_users.objects.get(pk=user_id))
            sum = Summarization.objects.get_or_create(question=med_question_list, sUser= current_users.objects.get(pk=user_id))
            print(sum)
            done_or_not.tdone = True
            print(done_or_not)
            done_or_not.save()
            
            return redirect(f'/questions/do_summary/{date}/{ques_id}/next/False')
    else:
        pass
    

    return render(request, 'questions/summary_ques_id.html', context)


@login_required
def next_data(request, date, ques_id, pure_next):
    try:
        if pure_next == 'True':
            ret = Question.objects.filter(qQuestion_ID__gt=ques_id, settask__tStartTime=date, settask__tUser=request.user.id).order_by("qQuestion_ID")[0:1].get().qQuestion_ID
        else:
            ret = Question.objects.filter(qQuestion_ID__gt=ques_id, settask__tStartTime=date, settask__tUser=request.user.id, settask__tdone=False).order_by("qQuestion_ID")[0:1].get().qQuestion_ID
    except:
        if pure_next == 'True':
            ret = Question.objects.filter(settask__tStartTime=date, settask__tUser=request.user.id).aggregate(Min("qQuestion_ID"))['qQuestion_ID__min']
        else:
            if Question.objects.filter(settask__tStartTime=date, settask__tUser=request.user.id, settask__tdone=False).count()==0:
                return redirect('/questions/')
            else:
                ret = Question.objects.filter(settask__tStartTime=date, settask__tUser=request.user.id).aggregate(Min("qQuestion_ID"))['qQuestion_ID__min']
    return redirect(f'/questions/do_summary/{date}/{ret}/')

@login_required
def prev_data(request, date, ques_id, pure_prev):
    try:
        if pure_prev == 'True':
            ret = Question.objects.filter(qQuestion_ID__lt=ques_id, settask__tStartTime=date, settask__tUser=request.user.id).order_by("-qQuestion_ID")[0:1].get().qQuestion_ID
        else:
            ret = Question.objects.filter(qQuestion_ID__lt=ques_id, settask__tStartTime=date, settask__tUser=request.user.id, settask__tdone=False).order_by("-qQuestion_ID")[0:1].get().qQuestion_ID
    except:
        if pure_prev == "True":
            ret = Question.objects.filter(settask__tStartTime=date, settask__tUser=request.user.id).aggregate(Max("qQuestion_ID"))['qQuestion_ID__max']
        else:
            if Question.objects.filter(settask__tStartTime=date, settask__tUser=request.user.id, settask__tdone=False).count()==0:
                return redirect('/questions/')
            else:
                ret = Question.objects.filter(settask__tStartTime=date, settask__tUser=request.user.id, setlabeltask__tdone=False).aggregate(Max("qQuestion_ID"))['qQuestion_ID__max']
    return redirect(f'/questions/do_summary/{date}/{ret}/')



#  user = User.objects.get(pk=request.session['id'])