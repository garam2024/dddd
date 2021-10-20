# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
import subprocess
import glob
# Create your views here.

from django.views import View
from django.conf import settings

from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from db_info import dbinfo

## 페이지 접속 시 로그인 체크 호출
from django.contrib.auth.decorators import login_required

# 기본 유저 관리 호출
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

## 유저 세션 처리용 호출
from django.contrib.auth import user_logged_in
from django.dispatch.dispatcher import receiver

# DB Table 호출
# from dtwo_video_convert import task_num
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


class adminTaskCheck(TemplateView):
    template_name = 'django_app/manage/adminview_interface_inspect.html'
    template_name2 = 'django_app/manage/adminview_abnormal_inspect.html'

    def __init__(self):
        self.res_dic = {}

    def get(self, request, *args, **kwargs):
        # is_superuser = UserAdapter().get_is_superuser(request)
        # primary_id = User.objects.get(username=request.user)
        #profile = Profile.objects.get(user_id=primary_id).account_id
        #
        # print("request.user확인!!", request.user)
        # print("is_superuser확인!!", is_superuser)
        # print("profile", profile)
        return redirect("/admin/index")

    def post(self, request, *args, **kwargs):

        # is_superuser = UserAdapter().get_is_superuser(request)
        # primary_id = User.objects.get(username=request.user)
        # profile = Profile.objects.get(user_id=primary_id).account_id
        #
        # print("request.user확인!!", request.user)
        # print("is_superuser확인!!", is_superuser)
        # print("profile", profile)



        # user_name = request.POST["worker_id"]
        work_id = request.POST["work_id"]
        work_type = request.POST["work_type"]
        work_status = request.POST["work_status"]

        if work_type == "interface":
            self.template_name = self.template_name

        elif work_type == "normal":
            self.template_name = self.template_name2

        ## 관리자 권한 체크
        # is_superuser = UserAdapter().get_is_superuser(request)

        task_info = TaskInfoAdapter().get_task_info_admin(request, work_id, work_status)
        message_context = "Exists"

        self.res_dic['task_info'] = task_info

        self.res_dic['message_info'] = message_context

        task_db_list = getTaskInfo().task_db_select_all2(work_id)
        self.res_dic['task_region'] = str(task_db_list)
    # else:
    #     messages.info(request,"관리자 권한이 필요합니다")
    #
    #     return redirect("main")



        return render(request, self.template_name, self.res_dic)


def admin_complete(request):
    print("admin_complete들어왔다.")
    if request.method == "POST":

        dict = json.loads(request.body)
        work_type = dict['work_type']
        work_id = dict['work_id']
        work_status = dict['work_status']
        work_status = str(work_status)

        if work_type == "interface":
            TaskInfoAdapter().admin_complete_check(request, work_id,work_status)

        elif work_type == "normal":
            TaskInfoAdapter().admin_complete_check_abnormal(request)

    return HttpResponse('success')


def task_api(request):

    if request.method == "POST":
        dict = json.loads(request.body)

        work_id = dict['work_id']
        task_num = work_id

        user_name = request.user
        print("task_num : " + str(task_num) + "UserName : " + str(user_name))
        getTaskInfo().get_task_db_insert(request, user_name, task_num)

        ## 정보가 없다고 하면 고유 ID and image Path
        ## 정보가 있다고 하면 JSON 정보만
        message = 1

        ret = {"message": message}

    return HttpResponse(json.dumps(ret), content_type="application/json")


def check_task(request):
    dict = json.loads(request.body)

    task_num = str(dict['work_id'])

    user_name = str(request.user)

    task_db_list = getTaskInfo().task_db_select(user_name, task_num)


    return HttpResponse(json.dumps(task_db_list), content_type="application/json")
