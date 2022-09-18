from multiprocessing import context
from django.http import FileResponse, HttpResponse, Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
import json, os
import datetime
from .settings import BASE_DIR
from question.models import Question, models, Summarization
class HomeView(TemplateView):
    template_name = 'home.html'


def process_byte_data(save_dir, data):
    with open(save_dir, 'wb')as destination:
        for chunk in data.chunks():
            destination.write(chunk)

def filter_summarized_data(element):
    single = element['single']
    often = element['often']
    multi = element['multi']
    discuss = element['discuss']

    if single and often:
        #often
        try:
            query = element['Query']
            question_type = element['Question_type']
            question_filter = 2
        except KeyError:
            print('資料有出錯')
            print(element['Original_ques_id'])
    elif single:
        try:
            query = element['Query']
            question_type = element['Question_type']
            question_filter = 1
        except KeyError:
            print('資料有出錯 single')
            print(element['Original_ques_id'])
    elif multi:
        #multi data
        question_filter = 3
        query = None
        question_type = 0
    elif discuss:
        #discuss data
        question_filter = 4
        query = None
        question_type = 0
    else:
        #trash data
        question_filter = 5
        query = None
        question_type = 0

    return question_filter, query, question_type


@user_passes_test(lambda u: u.is_superuser)
def upload_raw_json_data(request):
    Users_model = get_user_model() # 現有的users
    users = Users_model.objects.all()
    error = False
    error_msg = ''
    success = False
    success_msg = ''
    context = {
        'success': success,
        'success_msg': success_msg,
        'error': error,
        'error_msg': error_msg
    }
    if request.method == 'POST':
        json_file = request.FILES['jsonfile_upload']

        if json_file.name.split('.')[1] != 'json':
            context['error'] = True
            context['error_msg'] = "請上傳json格式!"
            return render(request, 'data/upload_raw_json_data.html', context)

        saved_json_file_name = 'medi_data_{}.json'.format(datetime.datetime.today().strftime("%Y-%m-%d"))
        saved_location = os.path.join(BASE_DIR, 'uploaded_data', saved_json_file_name)

        process_byte_data(saved_location, json_file)

        with open(saved_location, 'r', encoding='utf-8')as f:
            json_array = json.load(f)

        upload_data_num = len(json_array)
        new_data = 0
        old_data = 0
        for element in json_array:
            try:
                q_id = element['Original_ques_id']
                q_title = element['Title']
                q_ques = element['Original_question']
                question_qs, created = Question.objects.get_or_create(qQuestion_ID=q_id)

                if created:
                    #there is no same question id in DB, will be created new data
                    try:
                        q_filter, q_query, q_qtype = filter_summarized_data(element)
                        sum = Summarization.objects.create(question = question_qs, sUser = request.user)
                        sum.save()
                    except KeyError:
                        #IF NOT means haven't be watch before
                        q_filter = 0
                        q_query = ""
                        q_qtype = 0
                    question_qs.qQuestion_Title = q_title
                    question_qs.qOriginal_Question = q_ques
                    question_qs.sQuery = q_query
                    question_qs.sQuestion_Type = q_qtype
                    question_qs.sQuestion_Filter = q_filter
                    question_qs.save()
                    new_data += 1
                else:
                    old_data += 1

            except KeyError:
                context['error'] = True
                context['error_msg'] = 'json檔案中有keyword不符合規定格式！'
                return render(request, 'data/upload_raw_json_data.html', context)

        context['success'] = True
        context['success_msg'] = "總共有{}筆資料，其中新增{}筆，與現有的重疊有{}筆，請再去DB確認資料！".format(upload_data_num, new_data, old_data)
        
        return render(request, 'data/upload_raw_json_data.html', context)

        # print(json_array)
    

    return render(request, 'data/upload_raw_json_data.html', context)



def download_raw_json_data(request):
    datas = list(Question.objects.all().values())
    file_name = "C:/Users/howard/Desktop/mednet_server/download_data/medinet_download_{}.json".format(datetime.datetime.today().strftime("%Y-%m-%d"))
    with open(file_name, 'w', encoding = 'utf-8')as f:
        json.dump(datas, f, ensure_ascii=False, indent=4)
    if os.path.exists(file_name):
        with open(file_name, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/json")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_name)
            return response
    raise Http404
    