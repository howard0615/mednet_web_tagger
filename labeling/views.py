from turtle import done
from labeling.forms import labelQuestionForm, ReviewQuestionForm
from .models import Label
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from labeltask.models import SetLabelTask
import datetime
from django.db.models import Q
from question.models import Question
from django.db.models import Min, Max
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

@login_required
def your_label_tasks(request):
    if request.user.is_superuser:
        superuser = True
    else:
        superuser = False

    if request.user.is_authenticated:
        user_id = request.user.id
    
    your_label_tasks = SetLabelTask.objects.filter(tUser = user_id)
    your_task_in_diff_dates = your_label_tasks.values('tStartTime').distinct()

    data_situation = {}
    for data_task in your_task_in_diff_dates:
        if datetime.date.today() >= data_task['tStartTime']:
            d = SetLabelTask.objects.filter(tStartTime = data_task['tStartTime'], tUser=user_id)
            undone = d.filter(tdone=True)
            data_situation[data_task['tStartTime'].strftime("%Y-%m-%d")] = undone.count()/d.count()*100
        else:
            pass
    context = {
        "data_situation": data_situation,
        "superuser": superuser
    }
    return render(request, 'label/your_label_tasks.html', context)


@login_required
def label_date_rough_see(request, date):
    if request.user.is_authenticated:
        user_id = request.user.id

    if request.method == 'POST':
        print(request.POST['label_id'])
        return redirect(f'/label/do_label/{date}/{request.POST["label_id"]}/')
    else:
        undone = SetLabelTask.objects.filter(tUser = user_id, tdone = False).order_by('tQuestion__qQuestion_ID')
        done = SetLabelTask.objects.filter(tUser = user_id, tdone = True).order_by('tQuestion__qQuestion_ID')
        context = {
            'undone': undone,
            'done': done
        }
    return render(request, 'label/label_date_rough_see.html', context)


@login_required
def do_label(request, date, ques_id):
    if request.user.is_authenticated:
        user_id = request.user.id
    users_model = get_user_model()

    set_label_task = SetLabelTask.objects.get(tQuestion=ques_id, tUser = users_model.objects.get(pk=user_id))
    med_question_list = Question.objects.get(qQuestion_ID= ques_id, setlabeltask__tStartTime=date, setlabeltask__tUser=request.user.id)

    print("done?" + str(set_label_task.tdone))
    print(med_question_list)

    

    if set_label_task.tdone:
        done_or_not = True
        label = Label.objects.get(LUser = users_model.objects.get(pk=user_id), LLabel_task = set_label_task)
        label_form = labelQuestionForm(request.POST or None, initial={'LAdequacy': label.LAdequacy, 'LDeducibility': label.LDeducibility,
                                                                        'LAbstractive': label.LAbstractive, 'LNote': label.LNote})
    else:
        done_or_not = False
        label_form = labelQuestionForm(request.POST or None)

    context = {'error': False, 'error_msg': '', 
                'med_question_list': med_question_list, 
                'set_label_task': set_label_task,
                "label_form": label_form,
                "done_or_not": done_or_not,
                "date":date,
                "ques_id": ques_id}

    
    if request.method == "POST": #如果是以POST方式才處理
        label_form = labelQuestionForm(request.POST)
        if label_form.is_valid():  #通過forms驗證
            #med_question的資料

            if label_form.cleaned_data['LAdequacy'] <0 and label_form.cleaned_data['LAdequacy']>=2:
                context['label_form'] = label_form
                context['error'] = True
                context['error_msg'] = 'label只有0或1'
                return render(request, 'label/label_ques_id.html', context)

            if label_form.cleaned_data['LDeducibility'] <0 and label_form.cleaned_data['LDeducibility']>=2:
                context['label_form'] = label_form
                context['error'] = True
                context['error_msg'] = 'label只有0或1'
                return render(request, 'label/label_ques_id.html', context)

            if label_form.cleaned_data['LAbstractive'] <0 and label_form.cleaned_data['LAbstractive']>=2:
                context['label_form'] = label_form
                context['error'] = True
                context['error_msg'] = 'label只有0或1'
                return render(request, 'label/label_ques_id.html', context)

            if not set_label_task.tdone:
                label = Label.objects.create(LUser = users_model.objects.get(pk=user_id),
                                            LLabel_task = set_label_task,
                                            LAdequacy = label_form.cleaned_data['LAdequacy'],
                                            LDeducibility = label_form.cleaned_data['LDeducibility'],
                                            LAbstractive = label_form.cleaned_data['LAbstractive'],
                                            LNote = label_form.cleaned_data['LNote'])
            else:
                label.LAdequacy=label_form.cleaned_data['LAdequacy']
                label.LDeducibility=label_form.cleaned_data['LDeducibility']
                label.LAbstractive=label_form.cleaned_data['LAbstractive']
                label.LNote=label_form.cleaned_data['LNote']


            label.save()
            set_label_task.tdone = True
            set_label_task.save()
            return redirect(f'/label/do_label/{date}/{ques_id}/next/False/')

            #做這筆摘要的使用者資料
            
    else:
        pass
    

    return render(request, 'label/label_ques_id.html', context)


@login_required
def next_data(request, date, ques_id, pure_next):
    try:
        if pure_next == "True":
            ret = Question.objects.filter(qQuestion_ID__gt=ques_id, setlabeltask__tStartTime=date, setlabeltask__tUser=request.user.id).order_by("qQuestion_ID")[0:1].get().qQuestion_ID
        else:
            ret = Question.objects.filter(qQuestion_ID__gt=ques_id, setlabeltask__tStartTime=date, setlabeltask__tUser=request.user.id, setlabeltask__tdone=False).order_by("qQuestion_ID")[0:1].get().qQuestion_ID
    except:
        if pure_next == "True":
            ret = Question.objects.filter(setlabeltask__tStartTime=date, setlabeltask__tUser=request.user.id).aggregate(Min("qQuestion_ID"))['qQuestion_ID__min']
        else:
            if Question.objects.filter(setlabeltask__tStartTime=date, setlabeltask__tUser=request.user.id, setlabeltask__tdone=False).count()==0:
                return redirect('/label/')
            else:
                ret = Question.objects.filter(setlabeltask__tStartTime=date, setlabeltask__tUser=request.user.id).aggregate(Min("qQuestion_ID"))['qQuestion_ID__min']
    return redirect(f'/label/do_label/{date}/{ret}/')

@login_required
def prev_data(request, date, ques_id, pure_prev):
    try:
        if pure_prev == 'True':
            ret = Question.objects.filter(qQuestion_ID__lt=ques_id, setlabeltask__tStartTime=date, setlabeltask__tUser=request.user.id).order_by("-qQuestion_ID")[0:1].get().qQuestion_ID
        else:
            ret = Question.objects.filter(qQuestion_ID__lt=ques_id, setlabeltask__tStartTime=date, setlabeltask__tUser=request.user.id, setlabeltask__tdone=False).order_by("-qQuestion_ID")[0:1].get().qQuestion_ID

    except:
        if pure_prev == 'True':
            ret = Question.objects.filter(setlabeltask__tStartTime=date, setlabeltask__tUser=request.user.id).aggregate(Max("qQuestion_ID"))['qQuestion_ID__max']
        else:
            if Question.objects.filter(setlabeltask__tStartTime=date, setlabeltask__tUser=request.user.id, setlabeltask__tdone=False).count()==0:
                return redirect('/label/')
            else:
                ret = Question.objects.filter(setlabeltask__tStartTime=date, setlabeltask__tUser=request.user.id, setlabeltask__tdone=False).aggregate(Max("qQuestion_ID"))['qQuestion_ID__max']
    return redirect(f'/label/do_label/{date}/{ret}/')

@user_passes_test(lambda u: u.is_superuser)
def admin_review_labels(request, ques_id):
    context = {
        'error': ''
    }
    question = Question.objects.get(qQuestion_ID = ques_id)
    review_form = ReviewQuestionForm(instance=question,
                                        initial={
                                            'qOriginal_Question': question.qOriginal_Question,
                                                'sQuery': question.sQuery,
                                                'sQuestionType': question.sQuestion_Type
                                        })
    context['review_form'] = review_form
    try:
        labels = Label.objects.filter(LLabel_task__tQuestion = ques_id)
        labels_numbers = labels.count()
        context['question']=question
        context['labels']=labels
        context['labels_numbers']=labels_numbers
    except Label.DoesNotExist:
        context['error']='Does not exist'

    if request.method == "POST":
        
        review_form = ReviewQuestionForm(request.POST, instance=question)
        ques_filter_format = {'single': 1, 'often': 2, 'multi': 3, 'discuss': 4, 'trash': 5}
        if review_form.is_valid():
            Question_Filter = ques_filter_format[request.POST['ques_filter']]
            if Question_Filter==3:
                question.sQuestion_Filter = Question_Filter
            review_form.save()
            question.save()
        labels.update(LAdequacy=1, LDeducibility=1, LAbstractive=1, LNote="HAVE CHANGED")
        return redirect(f'/label/admin_review_labels/{ques_id}/next/True/')


    return render(request, 'label/admin_review_labels.html', context)

@login_required
def next_review_data(request, ques_id, pure_next):
    try:
        if pure_next == "True":
            ret = Question.objects.filter(qQuestion_ID__gt=ques_id, setlabeltask__tdone=True).filter(Q(setlabeltask__label__LAdequacy=0) | Q(setlabeltask__label__LDeducibility=0) | Q(setlabeltask__label__LAbstractive=0) | ~Q(setlabeltask__label__LNote=None)).order_by("qQuestion_ID")[0:1].get().qQuestion_ID
        else:
            ret = Question.objects.filter(qQuestion_ID__gt=ques_id, setlabeltask__tdone=True).filter(Q(setlabeltask__label__LAdequacy=0) | Q(setlabeltask__label__LDeducibility=0) | Q(setlabeltask__label__LAbstractive=0) | ~Q(setlabeltask__label__LNotee=None) & ~Q(setlabeltask__label__LNote="HAVE CHANGED")).order_by("qQuestion_ID")[0:1].get().qQuestion_ID
    except:
        if pure_next == "True":
            ret = Question.objects.filter(qQuestion_ID__gt=ques_id, setlabeltask__tdone=True).filter(Q(setlabeltask__label__LAdequacy=0) | Q(setlabeltask__label__LDeducibility=0) | Q(setlabeltask__label__LAbstractive=0) | ~Q(setlabeltask__label__LNote=None)).aggregate(Min("qQuestion_ID"))['qQuestion_ID__min']
        else:
            if Question.objects.filter(setlabeltask__tdone=True).count()==0:
                return redirect('/label/')
            else:
                ret = Question.objects.filter(qQuestion_ID__gt=ques_id, setlabeltask__tdone=True).filter(Q(setlabeltask__label__LAdequacy=0) | Q(setlabeltask__label__LDeducibility=0) | Q(setlabeltask__label__LAbstractive=0) | ~Q(setlabeltask__label__LNote=None) & ~Q(setlabeltask__label__LNote="HAVE CHANGED")).aggregate(Min("qQuestion_ID"))['qQuestion_ID__min']
    return redirect(f'/label/admin_review_labels/{ret}/')

@login_required
def prev_review_data(request, ques_id, pure_prev):
    try:
        if pure_prev == 'True':
            ret = Question.objects.filter(qQuestion_ID__lt=ques_id, setlabeltask__tdone=True).filter(Q(setlabeltask__label__LAdequacy=0) | Q(setlabeltask__label__LDeducibility=0) | Q(setlabeltask__label__LAbstractive=0) | ~Q(setlabeltask__label__LNote=None)).order_by("-qQuestion_ID")[0:1].get().qQuestion_ID
        else:
            ret = Question.objects.filter(qQuestion_ID__lt=ques_id, setlabeltask__tdone=True).filter(Q(setlabeltask__label__LAdequacy=0) | Q(setlabeltask__label__LDeducibility=0) | Q(setlabeltask__label__LAbstractive=0) | ~Q(setlabeltask__label__LNote=None) & ~Q(setlabeltask__label__LNote="HAVE CHANGED")).order_by("-qQuestion_ID")[0:1].get().qQuestion_ID

    except:
        if pure_prev == 'True':
            ret = Question.objects.filter(qQuestion_ID__lt=ques_id, setlabeltask__tdone=True).filter(Q(setlabeltask__label__LAdequacy=0) | Q(setlabeltask__label__LDeducibility=0) | Q(setlabeltask__label__LAbstractive=0) | ~Q(setlabeltask__label__LNote=None)).aggregate(Max("qQuestion_ID"))['qQuestion_ID__max']
        else:
            if Question.objects.filter(setlabeltask__tdone=True).count()==0:
                return redirect('/label/')
            else:
                ret = Question.objects.filter(qQuestion_ID__lt=ques_id, setlabeltask__tdone=True).filter(Q(setlabeltask__label__LAdequacy=0) | Q(setlabeltask__label__LDeducibility=0) | Q(setlabeltask__label__LAbstractive=0) | ~Q(setlabeltask__label__LNote=None) & ~Q(setlabeltask__label__LNote="HAVE CHANGED")).aggregate(Max("qQuestion_ID"))['qQuestion_ID__max']
    return redirect(f'/label/admin_review_labels/{ret}/')