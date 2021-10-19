# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

# Create your views here.

from django.views import View
from django.conf import settings


from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


## 페이지 접속 시 로그인 체크 호출
from django.contrib.auth.decorators import login_required

#기본 유저 관리 호출
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

## 유저 세션 처리용 호출
from django.contrib.auth import user_logged_in
from django.dispatch.dispatcher import receiver


# DB Table 호출
from ..models import *

import json, cv2, os, csv

from django.contrib import messages
## Controller import
from ..Controller.UserAdapter import *
from ..Controller.TaskAdapter import *
from ..Controller.TaskInfoAdapter import * 
from ..Controller.getTaskInfo import *
from ..Controller.InspectAdapter_1st import *
from ..Controller.InspectAdapter_2nd import *
from ..Controller.InspectAdapter_3rd import *
from ..Controller.adminAdapter import * 

from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from db_info import dbinfo

URL_LOGIN = 'index'
decorators = [csrf_exempt, login_required(login_url=URL_LOGIN)]



## [유저] 나의 작업 페이지 ( 재작업 기능 )
@method_decorator(login_required(login_url=URL_LOGIN), name='dispatch')
class My_Task(TemplateView):

    template_name = 'django_app/mytask.html'
         
    def __init__(self):
        self.res_dic = {}
        
        
    def get(self, request, *args, **kwargs):

        ## 기본 메인 페이지

        task_table_list = TaskAdapter().get_my_task_list(request)
        inspect_table_list = InspectAdapter_1st().get_my_inspect_list(request)
        inspect_table_list_2 = InspectAdapter_2nd().get_my_inspect_list(request)
        inspect_table_list_3 = InspectAdapter_3rd().get_my_inspect_list(request)

        self.res_dic['task_list'] = task_table_list
        self.res_dic['inspect_list'] = inspect_table_list
        self.res_dic['inspect_list_2'] = inspect_table_list_2
        self.res_dic['inspect_list_3'] = inspect_table_list_3

        get_user_name = UserAdapter().get_profile(request)
        self.res_dic['profile'] = get_user_name

        print("전역변수 코드 테스트--------------------------------------------")
        print(getattr(settings, 'GLOBAL_CODE', None))

        return render(request, self.template_name, self.res_dic)

def bring_memo(request):
    dict = json.loads(request.body)
    work_id = dict.get('work_id')
    sql = sqlMethod()
    result = sql.select_workList('django_app_worklist', {'work_id': str(work_id)}, None, ['reg_id', 'group_id'])

    reg_id = result[0]['reg_id']
    group_id = result[0]['group_id']

    dic = {
        'daw.work_id': str(work_id),
        # 'daw.reg_id': str(reg_id),
        'daw.group_id': str(group_id)
    }

    string = 'django_app_workhistory daw left outer join django_app_tasklist dat on daw.work_id = dat.work_id and daw.group_id = dat.group_id'
    bringMemo = sql.select_workList(string, dic, None, ['memo'], None)
    print(bringMemo)
    # print(len(bringMemo))
    #
    # _messages: ''
    #
    # for index in bringMemo:
    #     if index['memo'] != None:
    #         _messages += index['memo']
    #
    # print('추가')
    # print(_messages)

    return JsonResponse(bringMemo, safe=False)


## [유저] 전체 작업 내역 페이지
@method_decorator(login_required(login_url=URL_LOGIN), name='dispatch')
class My_Task_Record(TemplateView):

    template_name = 'django_app/mytask_record.html'
         
    def __init__(self):
        self.res_dic = {}
        
        
    def get(self, request, *args, **kwargs):

        ## 기본 메인 페이지

        task_record_list, inspect_record_list = getTaskInfo().get_task_record(request)

        self.res_dic['task_record_list'] = task_record_list
        self.res_dic['inspect_record_list'] = inspect_record_list

        get_user_name = UserAdapter().get_profile(request)
        self.res_dic['profile'] = get_user_name


        return render(request, self.template_name, self.res_dic)

        

def task_cancel_module(request, task_num):

    if request.method == "POST" :

        get_message = str(TaskInfoAdapter().task_cancel(request, task_num))

        print("task_cancel_module Activate")

        if get_message == "True":

            return redirect('mywork')

        else:
            messages.info(request, dbinfo.message["mes_work_cancel_error"])

            return redirect('mywork')




## [유저] 검수 취소 모듈
def inspect_cancel_module_1st(request, task_num):

    if request.method == "POST" :

        get_message = str(InspectAdapter_1st().inspect_cancel(request, task_num))

        print("inspect_cancel_module_1st Activate")

        if get_message == "True":

            return redirect('mywork')

        else:
            messages.info(request, dbinfo.message["mes_inspect_cancel_error"])

            return redirect('mywork')



## [유저] 검수 취소 모듈
def inspect_cancel_module_2nd(request, task_num):

    if request.method == "POST" :

        get_message = str(InspectAdapter_2nd().inspect_cancel(request, task_num))

        print("inspect_cancel_module_2nd Activate")

        if get_message == "True":

            return redirect('mywork')

        else:
            messages.info(request, dbinfo.message["mes_inspect_cancel_error"])

            return redirect('mywork')



## [유저] 검수 취소 모듈
def inspect_cancel_module_3rd(request, task_num):

    if request.method == "POST" :

        get_message = str(InspectAdapter_3rd().inspect_cancel(request, task_num))

        print("inspect_cancel_module_3rd Activate")

        if get_message == "True":

            return redirect('mywork')

        else:
            messages.info(request, dbinfo.message["mes_inspect_cancel_error"])

            return redirect('mywork')



def Re_Task_process(self, request, task_num, worktype):

    if worktype =='normal':
        template_name = 'django_app/re_task_process_abnormal.html'
    else :
        template_name = 'django_app/re_task_process.html'


    user_name = str(request.user)

    get_message = TaskInfoAdapter().rework_logic(request, user_name, task_num)
    staff_permission = UserAdapter().get_is_staff(request)

    get_message = str(get_message)
    print(get_message)

    res_dic ={}

    if staff_permission:
        if get_message == '4':
            print("!!!!!!!!!!!!!!!!!4!!!!!!!!!!!!!!!!!!!!!!")
            task_info_list = TaskInfoAdapter().get_task_info(request, user_name, task_num)
            message_context = "Exists"

            res_dic['task_info_list'] = task_info_list
            res_dic['message_info'] = message_context



            return render(request, template_name, res_dic)

        elif get_message == '304':

            print("작업은 1개씩만 할 수 있습니다.")

            messages.info(request, dbinfo.message["mes_inspect_max_1"])

            return redirect('mywork_record')

        else:

            messages.info(request, dbinfo.message["mes_error"])

            return redirect('main')

    else:

        messages.info(request, dbinfo.message["mes_work_auth_needed"])

        return redirect("mywork")