# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

# Create your views here.

from django.views import View
from django.conf import settings


from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.http import Http404
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
from ..Controller.sqlMethod import *

from datetime import datetime

# Import mimetypes module
import mimetypes
# Import HttpResponse module
from django.http.response import HttpResponse

from django.conf import settings
from db_info import dbinfo

URL_LOGIN = 'index'
decorators = [csrf_exempt, login_required(login_url=URL_LOGIN)]




## [유저] 작업 신청 시 접속되는 기본 작업 페이지
@method_decorator(login_required(login_url=URL_LOGIN), name='dispatch')
class Task_process(TemplateView):

    template_name = 'django_app/task_process.html'
    
    def __init__(self):
        self.res_dic = {}

    def get(self, request, *args, **kwargs):

        print("task_process get")

        return redirect("/")

    def post(self, request, task_num, *args, **kwargs):

        user_name = str(request.user)
        # task_num

        staff_permission = UserAdapter().get_is_staff(request)
        staff_permission = staff_permission
        print("staff_permission : ", staff_permission)
        if staff_permission :

            get_message = TaskInfoAdapter().change_db_info(request, user_name, task_num)
            get_message = str(get_message)

            print("Message : ", get_message)

            if get_message == 'True':
                
                task_info = TaskInfoAdapter().get_task_info(request, user_name, task_num).first()

                # server side file download

                # print("1. task_info : ", task_info)
                # video_name = task_info.video_path
                # print("2. video_name : ", video_name)
                # test_video_path = "/code/django_project" + video_name
                # print("3. file_path : ", test_video_path)

                # if os.path.exists(test_video_path):
                #     print('파일 있음')
                #     with open(test_video_path, 'rb') as fh:
                #         response = HttpResponse(fh.read(), content_type="application/force_download")
                #         response['Content-Disposition'] = 'inline; filename=' + os.path.basename(test_video_path)
                #         return response
                # # If file is not exists
                # raise Http404

                # file_name = video_name.split('/')
                # self.res_dic['fileName'] = file_name[len(file_name)-1]
                # self.res_dic['video_name'] = video_name


                task_db_list = getTaskInfo().task_db_select_all(user_name, task_num)
                self.res_dic['task_region'] = str(task_db_list)

                self.res_dic['task_info'] = task_info
                self.res_dic['task_num'] = task_num


                return render(request, self.template_name, self.res_dic)

            elif get_message == '304' :

                print("작업은 1개씩만 할 수 있습니다.")

                messages.info(request, dbinfo.message["mes_work_max_1"])
                return redirect("task_list")

            elif get_message == "404" :

                print("잘못된 접근인 경우")
                
                messages.info(request, dbinfo.message["mes_already_allocation_work"])
                return redirect('mywork')
            
            elif get_message == "False" :
                
                print("이미 할당된 작업인 경우")
                
                messages.info(request, dbinfo.message["mes_already_allocation_work"])
                return redirect('task_list')
                
        else:

            messages.info(request, dbinfo.message["mes_work_auth_needed"])
            return redirect("task_list")




## [유저] 나의 작업 페이지에서 신청 시 접속되는 재 작업 페이지
@method_decorator(login_required(login_url=URL_LOGIN), name='dispatch')
class Re_Task_process(TemplateView):

    template_name = 'django_app/re_task_process.html'
    template_name1 = 'django_app/re_task_process_abnormal.html'
    
    def __init__(self):
        self.res_dic = {}

    def get(self, request, *args, **kwargs):

        print("retask_process get")

        return redirect("/")

    def post(self, request, task_num, work_type, *args, **kwargs):

        if work_type == "normal":
            self.template_name = self.template_name1

        user_name = str(request.user)

        get_message = TaskInfoAdapter().rework_logic(request, user_name, task_num)
        staff_permission = UserAdapter().get_is_staff(request)

        get_message = str(get_message)
        
        if staff_permission:

            if get_message == '4':

                task_info = TaskInfoAdapter().get_task_info(request, user_name, task_num)
                message_context = "Exists"

                self.res_dic['task_info'] = task_info
                self.res_dic['message_info'] = message_context
                ##경진
                history_info = TaskInfoAdapter().get_history_info(task_num)
                self.res_dic['history_info'] = history_info
                
                task_db_list = getTaskInfo().task_db_select_all(user_name, task_num)
                self.res_dic['task_region'] = str(task_db_list)

                return render(request, self.template_name, self.res_dic)
            
            elif get_message == '5':

                message_context = "NotExists"

                self.res_dic['message_info'] = message_context

                return render(request, self.template_name, self.res_dic)

            elif get_message == '304':

                print("작업은 1개씩만 할 수 있습니다.")

                messages.info(request, dbinfo.message["mes_work_max_1"])

                return redirect('mywork_record')

            else:

                messages.info(request, dbinfo.message["mes_error"])

                return redirect('main')
        
        else : 

            messages.info(request, dbinfo.message["mes_work_auth_needed"])

            return redirect("mywork")

    


# ## [유저] 작업 취소 모듈
# def task_cancel_module(request, task_num):

#     if request.method == "POST" :

#         get_message = str(TaskInfoAdapter().task_cancel(request, task_num))

#         print("task_cancel_module Activate")

#         if get_message == "True":

#             return redirect('mytask')

#         else:
#             messages.info(request, '작업 취소 기능 오류')

#             return redirect('mytask')


## [유저] 작업 완료 시 DB 정보 갱신 모듈
def task_complete_module(request, task_num, work_type):

    print('도착')
    if request.method == "POST":
        print('==========')
        print(task_num)

        TaskInfoAdapter().task_complete_check(request, task_num)

        print("task_complete_module Activate")

        message = "success"
        ret = {"message": message}

        return HttpResponse(json.dumps(ret), content_type="application/json", status=200)



## [유저] 작업 페이지내에서 동작하는 중간 취소 모듈
def task_middle_cancel_module(request, task_num, work_type):

    if request.method == "POST" :

        get_message = str(TaskInfoAdapter().task_middle_cancel(request, task_num))

        print("task_middle_cancel_module Activate")

        if get_message == "True":
            message = {"message":"success"}

            return HttpResponse(json.dumps(message), content_type = "application/json", status = 200)

        else:
            messages.info(request, dbinfo.message["mes_work_cancel_error"])
            message = {"message":"failed"}

            return HttpResponse(json.dumps(message), content_type = "application/json", status = 200)
            



## [유저] 작업 정보 요청(갱신) 및 정보 반환 모듈
def info_api(request):
    ## POST 값을 가져옴
    get_unique_id=request.POST.get('nid')

    query_set = WorkList.objects.all()

    ## 프론트에서 보내주는 WorkList의 primary_key 값
    get_task_value = WorkList.objects.get(task_num = get_unique_id)
    
    
    for user in user_list:
        if(nid==user.username and nid !=""):
            message=0
    ret={"message":message}

    return HttpResponse(json.dumps(ret), content_type="application/json")


## [유저] My_Task 페이지 접속 시 무조건 처음에 DB 데이터를 한번 요청
def check_api(request, task_num, work_type):

    print("task_num : ", task_num)
    user_name = str(request.user)


    recombine_dict, get_images_list = getTaskInfo().check_db_data(request, user_name, task_num)
    
    ret_list = []
    ret_list.append(recombine_dict)
    ret_list.append("&")
    ret_list.append(get_images_list)


    return HttpResponse(ret_list, {'success' : True}, status = 200)


## [유저] 작업 정보 확인 모듈
def check_task(request, task_num, work_type):
    user_name = str(request.user)
    task_num = task_num

    task_db_list = getTaskInfo().task_db_select(user_name, task_num)

    return HttpResponse(json.dumps(task_db_list), content_type="application/json")


## [유저] 작업, 검수 페이지에서 번호 이동 시 번호별 데이터 저장용 모듈
def task_api(request, task_num, work_type):
    ## POST 값을 가져옴

    user_name = request.user
    print("user_name : " + str(user_name))
    print("task_num : " + str(task_num))

    # print(json.loads(request.body).get('attributes'))
    getTaskInfo().get_task_db_insert(request, user_name, task_num)

    ## 정보가 없다고 하면 고유 ID and image Path
    ## 정보가 있다고 하면 JSON 정보만
    message = 1

    ret = {"message": message}

    return HttpResponse(json.dumps(ret), content_type="application/json")




## [유저] 작업, 검수 페이지에서 Region 삭제 시 db instance 번호 이동 시 번호별 데이터 저장용 모듈
def task_region_delete(request, task_num, work_type):
    ## POST 값을 가져옴
    try:
        user_name = request.user
        task_num = task_num

        print("task_num : " + str(task_num))
        print("UserName : " + str(user_name))

        if work_type == "normal":
            getTaskInfo().task_db_delete_abnormal(request, user_name, task_num)
        else:
            getTaskInfo().task_db_delete(request, user_name, task_num)

        ## 정보가 없다고 하면 고유 ID and image Path
        ## 정보가 있다고 하면 JSON 정보만
        message = 1

        ret = {"message": message}

        return HttpResponse(json.dumps(ret), content_type="application/json")
    except Exception as e:
        ret = {"message": e}
        return HttpResponse(json.dumps(ret), content_type="application/json")




def task_region_delete_abnormal(request, task_num, work_type):
    ## POST 값을 가져옴

    try:
        user_name = request.user
        task_num = task_num

        print("task_num : " + str(task_num))
        print("UserName : " + str(user_name))

        getTaskInfo().task_db_delete_abnormal(request, user_name, task_num)

        ## 정보가 없다고 하면 고유 ID and image Path
        ## 정보가 있다고 하면 JSON 정보만
        message = 1

        ret = {"message": message}

        return HttpResponse(json.dumps(ret), content_type="application/json")
    except Exception as e:
        ret = {"message": e}
        return HttpResponse(json.dumps(ret), content_type="application/json")