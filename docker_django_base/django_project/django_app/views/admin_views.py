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
#from dtwo_video_convert import task_num
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
from django.http import JsonResponse
from db_info import dbinfo

'''
@@ START :  ---------------------- 관리자 페이지 View -------------------------------
'''


## [관리자] 기본 페이지

class adminIndex(TemplateView):
    template_name = 'django_app/manage/admin_index.html'

    def __init__(self):
        self.res_dic = {}

    def get(self, request, *args, **kwargs):

        # ## 관리자 권한 체크
        is_superuser = UserAdapter().get_is_superuser(request)
        # whatGroup = UserAdapter().get_group(request)
        print('profile')
        print('profile')
        print('profile')
        print('profile')
        print('profile')
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        # print(whatGroup)

        # print(request.user.is_authenticated)

        if request.user.is_authenticated and is_superuser:

            print('admin Index GET Activate')
            # if whatGroup == '-':
            user_list = adminAdapter().getUserList(request)
            print("user_list------------------------------------------------------------------------")
            self.res_dic['user_list'] = user_list
            #     print("---------------------------------------------------------------------------------")
            if whatGroup['group_id'] != '-': # 그룹별
                groupData = adminAdapter().getGroupInfo(request, whatGroup['group_id'])
                self.res_dic = groupData
                # 여기
                print("geteif11111111111111", dbinfo.status)

<<<<<<< .mine
            res_dic = adminAdapter().getProjectProgress(request)
            print("res_dic--------------------------------------------------------------------------")
            print(res_dic)
            self.res_dic.update(res_dic)
            print("---------------------------------------------------------------------------------")
||||||| .r259
            data = adminAdapter().getGroupInfo(request, whatGroup['group_id'])
            res_dic = adminAdapter().getProjectProgress(request)
            self.res_dic.update(res_dic)
            self.res_dic['user_list'] = data['user_list']
            self.res_dic['total_worklist'] = data['total_worklist']
            self.res_dic['all_task_list'] = data['all_task_list']
=======
            else: # '-' 전체 정보
                user_list = adminAdapter().getUserList(request)
                all_task_list = adminAdapter().get_current_process(request)
>>>>>>> .r284

<<<<<<< .mine
            all_task_list = adminAdapter().get_current_process(request)
            print("all_task_list--------------------------------------------------------------------")
            # check_task_list = adminAdapter().get_task_check_data(request)
            print("check_task_list--------------------------------------------------------------------")
            #     print(all_task_list)
            #     print("check_task_list------------------------------------------------------------------")
            #     print(check_task_list)
            self.res_dic['all_task_list'] = all_task_list
            # self.res_dic['check_task_list'] = check_task_list
            #     print("---------------------------------------------------------------------------------")

            print("self.res_dic!!!!!!!!-----------------------------------------------------------------------")
            # print(self.res_dic)

||||||| .r259
=======
                self.res_dic['user_list'] = user_list
                self.res_dic['all_task_list'] = all_task_list
                self.res_dic["gogo"] = dbinfo.status
                print("getelse11111111111111", dbinfo.status)


            res_dic = adminAdapter().getProjectProgress(request) #작업 현황(?)
            self.res_dic.update(res_dic) #업데이트로 딕셔너리 병합
            self.res_dic["dbinfostatus"] = dbinfo.status
            scores = dbinfo.status
            workviewList2 = ['status_work_deagi', 'status_1cha_companion_cansel','status_2cha_companion_cansel','status_job_cansel'
                             ,'status_3cha_companion_cansel','status_complet']
            scores.values()
            workviewOk = []
            for i in workviewList2:
                if i in scores:
                    value = scores[i]
                    workviewOk.append(value)
            # workviewOk = {name:score for name, score in scores.items() if name in workviewList2}
            print("workviewOk!!!!!!!!!!!", type(workviewOk))

            self.res_dic['workviewConfirm'] =workviewOk
            # 로그인 여기!!!!!서 찍힌다
            print("get11111111111111", dbinfo.status)
>>>>>>> .r284
            return render(request, self.template_name, self.res_dic)
            # elif whatGroup = 'tbit':
            #     pass
            #
            # elif whatGroup = 'gjac':
            #     pass
            #
            # elif whatGroup = 'dtw':
            #     pass

        else:

            messages.info(request, dbinfo.message["mes_admin_auth_need"])

            return redirect("main")

    def post(self, request, *args, **kwargs):

        print("POST -------------------------------------------------")
        data_dic = {
            "workerNm": request.POST.get('workerNm'),
            "workType": request.POST.get('workType'),
            "workStatus": request.POST.get('workStatus'),
            "searchBgn": request.POST.get('searchBgn'),
            "searchEnd": request.POST.get('searchEnd')
        }
        print(data_dic)
        dataCnt=0
        for key in data_dic.keys():
            if data_dic[key] != '':
                dataCnt += 1


        is_superuser = UserAdapter().get_is_superuser(request)

        get_message = str(adminAdapter().user_info_change(request))

        if get_message == "True" or dataCnt !=0 :

            if is_superuser:

                user_list = adminAdapter().getUserList(request)

                print(adminAdapter().getProjectProgress(request))
                # task_process, inspect_process, task_count, inspect_count = adminAdapter().getProjectProgress(request)

                prj_progress = adminAdapter().getProjectProgress(request)
                # 전체 작업수
                total_worklist_len = prj_progress['total_worklist_len']
                # 작업 대기 수
                task_ready_len = prj_progress['task_ready_len']
                # 전체 완료 수
                task_complete_len = prj_progress['task_complete_len']
                # 작업 진행 수
                task_working_len = prj_progress['task_working_len']
                # 전체 진행율
                # tatal_rate= prj_progress['tatal_rate']
                # 작업 완료 수

                # 1차 검수 대기 수
                inspect1_ready_len = prj_progress['inspect1_ready_len']
                # 2차 검수 대기 수
                inspect2_ready_len = prj_progress['inspect2_ready_len']
                # 3차 검수 대기 수
                inspect3_ready_len = prj_progress['inspect3_ready_len']
                # 1차 검수 진행 수
                inspect1_working_len = prj_progress['inspect1_working_len']
                # 2차 검수 진행 수
                inspect2_working_len = prj_progress['inspect2_working_len']
                # 3차 검수 진행 수
                inspect3_working_len = prj_progress['inspect3_working_len']
                
                print('total_worklist_lenㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
                print(total_worklist_len)
                # task_process = float(task_process) * 100
                # inspect_process = float(inspect_process) * 100
                # task_count = int(task_count)
                # inspect_count = int(inspect_count)

                # print("Check : " + str(task_process) + ' | ' + str(inspect_process) + ' | ' + str(task_count) + ' | ' + str(inspect_count))

                # # self.res_dic['task_process','inspect_process','task_count','inspect_count'] = task_process, inspect_process, task_count, inspect_count
                # self.res_dic['task_process'] = task_process
                # self.res_dic['inspect_process'] = inspect_process
                # self.res_dic['task_count'] = task_count
                # self.res_dic['inspect_count'] = inspect_count

                self.res_dic['total_worklist_len'] = total_worklist_len
                self.res_dic['task_ready_len'] = task_ready_len
                self.res_dic['task_working_len'] = task_working_len
                self.res_dic['task_complete_len'] = task_complete_len
                self.res_dic['inspect1_ready_len'] = inspect1_ready_len
                self.res_dic['inspect2_ready_len'] = inspect2_ready_len
                self.res_dic['inspect3_ready_len'] = inspect3_ready_len
                self.res_dic['inspect1_working_len'] = inspect1_working_len
                self.res_dic['inspect2_working_len'] = inspect2_working_len
                self.res_dic['inspect3_working_len'] = inspect3_working_len
                # self.res_dic['inspect_complete_len'] = inspect_complete_len
                # self.res_dic['tatal_rate'] = tatal_rate

                self.res_dic['user_list'] = user_list
                self.res_dic["dbinfo.status"] = dbinfo.status
                print("post11111111111111", dbinfo.status)
                try:
                    all_task_list = adminAdapter().get_current_process(request, data_dic=data_dic)
                    check_task_list = adminAdapter().get_task_check_data(request)

                    self.res_dic['all_task_list'] = all_task_list
                    self.res_dic['check_task_list'] = check_task_list
                    self.res_dic['statusDic'] = dbinfo.status
                    print("posttry11111111111111", dbinfo.status)


                    return render(request, self.template_name, self.res_dic)
                except:
                    raise

            else:

                messages.info(request, dbinfo.message["mes_admin_auth_need"])

                return redirect("main")

        else:
            messages.error(request, '정보 갱신 실패')

            return redirect("admin_index")

def changeAuth(request):
    dic = json.loads(request.body)
    print('상태 변경ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
    print(dic)
    sql = sqlMethod()

    value = {
        'is_staff': str(dic['workAuth']).lower(),  # 작업자
        'is_inspector': str(dic['inspectAuth']).lower()  # 검수
    }

    condition = {
        'account_id': str(dic['worker_id'])
    }

    value_1 = {
        'is_staff': str(dic['workAuth']).lower(),  # 작업자
        'is_active': 'true'  # 검수
    }

    condition_1 = {
        'username': str(dic['worker_id'])
    }

    selectOption = {
        'account_id': str(dic['worker_id']),
        'is_staff': str(dic['workAuth']).lower(),  # 작업자
        'is_inspector': str(dic['inspectAuth']).lower()  # 검수
    }

    sql.update_status('django_app_profile', value, condition)
    sql.update_status('auth_user', value_1, condition_1)
    result = sql.select_workList('django_app_profile', selectOption, None, None, None)
    print(result)
    if result[0]['is_staff'] == dic['workAuth'] and result[0]['is_inspector'] == dic['inspectAuth']:
        result = True
    else:
        result = False

    return HttpResponse(result)

def getSearchData(request):
    dic = json.loads(request.body)
    print('getSearchDataㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
    print(dic)
    # sql = sqlMethod().select_workList('django_app_worklist', )

    #작업자 이름 workNm
    for key in dic:
        if(dic[key] == ''):
            dic[key] == None

            # sql = sqlMethod().select_workList('django_app_worklist', dic)

    print(dic)

    if len(dic) == 0:
        return JsonResponse({'messages': 'false'}, safe=False)
    else:
        #worker_id
        #work_type
        #work_status
        result = adminAdapter().get_current_process(request, dic)
        return JsonResponse(result, safe=False)

## [관리자] 작업 확인 페이지

# class adminTaskCheck(TemplateView):

#     template_name = 'django_app/manage/admin_task_check.html'

#     def __init__(self):
#         self.res_dic = {}

#     ## 그냥 페이지를 들어갈 일이 없으므로 post 요청만 존재하면 됨

#     def post(self, request, task_num):

#         ## 관리자 내 작업 체크 페이지

#         is_superuser = UserAdapter().get_is_superuser(request)

#         if request.user.is_authenticated and is_superuser:

#             get_message = str(adminAdapter().task_rework_logic(request, task_num))

#             if get_message == "True" : 

#                 task_info_list = adminAdapter().get_task_info(request, task_num)
#                 message_context = "Exists"

#                 self.res_dic['task_info_list'] = task_info_list
#                 self.res_dic['message_info'] = message_context
#                 print('admin Task Check  POST Activate')

#             else :

#                 message_context = 'NotExists'
#                 self.res_dic['message_info'] = message_context


#             return render(request, self.template_name, self.res_dic)

#         else:

#             messages.info(request, '관리자 권한이 필요합니다.')

#             return redirect("main")


# ## [관리자] 검수 확인 페이지 
# class adminInspectCheck(TemplateView):

#     template_name = 'django_app/manage/admin_inspect_check.html'

#     def __init__(self):
#         self.res_dic = {}

#     ## 그냥 페이지를 들어갈 일이 없으므로 post 요청만 존재하면 됨

#     def post(self, request, task_num):
#         ## 관리자 내 검수 체크 페이지


#         is_superuser = UserAdapter().get_is_superuser(request)

#         if request.user.is_authenticated and is_superuser:

#             get_message = str(adminAdapter().inspect_rework_logic(request, task_num))

#             if get_message == "True" : 

#                 task_info_list = adminAdapter().get_inspect_info(request, task_num)

#                 message_context = "Exists"

#                 self.res_dic['task_info_list'] = task_info_list
#                 self.res_dic['message_info'] = message_context
#                 print('admin Inpsect Check  POST Activate')

#             else :

#                 message_context = "NotExists"

#                 self.res_dic['message_info'] = message_context


#             return render(request, self.template_name, self.res_dic)

#         else:

#             messages.info(request, '관리자 권한이 필요합니다.')

#             return redirect("main")


'''
** END :  ------------------------ 관리자 페이지 View -------------------------------
'''

'''
@@ START :  ---------------------- 관리자 페이지 Module -------------------------------
'''


## [관리자] 작업 승인 모듈
def admin_task_approve_module(request, record_key):
    if request.method == "POST":

        message = "approve"

        print("관리자 페이지 작업 승인 모듈 동작")

        message_2 = str(adminAdapter().task_status_change(request, record_key, message))

        if message_2 == "200":
            messages.info(request, dbinfo.message["mes_work_already_success"])

        return redirect("admin_index")


## [관리자] 작업 반려 모듈
def admin_task_cancel_module(request, record_key):
    if request.method == "POST":

        print("관리자 페이지 작업 반려 모듈 동작")

        message = "cancel"

        ## 반려 메시지
        refuse_message = str(request.POST.get('fix_text', ""))

        result_message = str(adminAdapter().task_deny_message_insert(request, record_key, refuse_message))

        print("result Message : ", result_message)

        message_2 = str(adminAdapter().task_status_change(request, record_key, message))

        if message_2 == "200" and result_message == "True":
            messages.info(request, dbinfo.message["mes_work_already_Companion"])

        return redirect("admin_index")


## [관리자] 유저 정보 갱신 모듈
# def admin_update_module(request):

#     if request.method == "POST":

#         task_num = request.POST.get('product')

#         tasker, inspector, task_process, inspect_process = adminAdapter().get_detail_info(request, task_num)

#         message = {"tasker_id": tasker, "inspector_id":inspector, "task_process":task_process,"inspect_process":inspect_process}

#         return HttpResponse(json.dumps(message), content_type = "application/json", status = 200)


## [관리자] 작업 확인 페이지의 DB 데이터 요청 모듈
def task_check_api(request, task_num):
    print("prouct_name : ", task_num)

    ## Task Check

    recombine_dict, get_images_list = adminAdapter().task_check_db_data(request, task_num)

    ret_list = []
    ret_list.append(recombine_dict)
    ret_list.append("&")
    ret_list.append(get_images_list)

    return HttpResponse(ret_list, {'success': True}, status=200)


## [관리자] 검수 확인 페이지의 DB 데이터 요청 모듈
def inspect_check_api(request, task_num):
    print("prouct_name : ", task_num)

    ## Inspect Check 

    recombine_dict, get_images_list = adminAdapter().inspect_check_db_data(request, task_num)

    ret_list = []
    ret_list.append(recombine_dict)
    ret_list.append("&")
    ret_list.append(get_images_list)

    return HttpResponse(ret_list, {'success': True}, status=200)


# 상민
def insert_work(request):
    try:
        print('______________________________insert_work 작동________________________________________')

        # 리눅스 명령어 실행 - 없는 것만 찾는 명령어
        # 결과 값에서 패스 수정
        # insert 명령문
        # find 경로
        path = r'/code/django_project/media/django_app/action_video/*.mp4'
        # subprocess.call(['find', path, '-name', '*_i'])

        # select_workList(self, data_dic, status_list)
        # insert_workList(self, table_name, data_dic)
        # update_status(self, status , work_id)

        # 읽기
        # path = '/mnt/disk2/vehicle_task_2/docker_django_base/django_project/media/django_app/action_video/' #어드민 파이 기준
        # #not
        # #find . -type f -and ! -name main.cpp -and ! -name *.h
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # cmd = ['sudo','find', path, ' -type f -and ! -name "*_Y.mp4"']
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        # fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
        # print("###########################################################")
        # data = str(fd_popen.read().strip())
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        # fd_popen.close()
        # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        # file_name = r'*.mp4'
        # fd_popen = subprocess.Popen(['find',' /code/django_project/media/django_app/action_video/ -type f -and ! -name *_Y.mp4'], stdout=subprocess.PIPE).stdout
        org_file_path = '/code/django_project/media/django_app'
        folder_list = ['/action_video/dtw/', '/action_video/tbit/', '/action_video/gjac/', '/abnormal_video/dtw/',
                       '/abnormal_video/tbit/', '/abnormal_video/gjac/']
        for key in folder_list:
            print("___________폴더 탐색 시작___________________________________________")
            command = 'find ' + org_file_path + key + ' -type f -and ! -name *_Y.mp4'
            fd_popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            (stdoutdata, stderrdata) = fd_popen.communicate()
            print("____________폴더 탐색 끝_____________________________________")

            data = stdoutdata.decode('utf-8')

            data = data.replace("\n", "^")
            file_list = data.split("^")

            print("파일갯수 : ", len(file_list))

            sql = sqlMethod()
            for file in file_list:
                file_org_name = file.strip()
                if len(file_org_name) == 0:
                    continue

                file_trans_name = file.replace('.mp4', '_Y.mp4')
                print('파일 원본 비디오명 : ', file_org_name, ' 파일 변경 비디오명 : ', file_trans_name)
                file_trans_name_last = file_trans_name.split('/')[-1]
                data_dic = {
                    'video_path': '/media/django_app' + key + file_trans_name_last,
                }

                result = sql.select_workList('django_app_worklist', data_dic=data_dic, column_list=['work_id'])
                print("..........", result)

                group_id = 'gjac'
                if 'dtw' in key:
                    group_id = 'dtw'
                elif 'tbit' in key:
                    group_id = 'tbit'
                else:
                    group_id = 'gjac'
                # 인설트
                if len(result) == 0:
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    data_dic = {
                        'work_type': 'interface' if 'action_video' in key else 'normal',
                        'video_path': data_dic["video_path"],
                        'work_status':dbinfo.status['status_work_deagi'],
                        'reg_id': 'admin',
                        'reg_date': now,
                        'group_id': group_id
                    }

                    history_dic = {
                        "work_id": "@$currval('django_app_worklist_task_num_seq')",
                        "work_status": dbinfo.status['status_work_deagi'],
                        "reg_id": "admin",
                        "reg_date": now,
                        "group_id": group_id
                    }
                    print("..........999")
                    sql.insert_workList(table_name='django_app_worklist', data_dic=data_dic)
                    print(
                        "---------------------------------------worklist insert complete--------------------------------------")
                    sql.insert_workList(table_name="django_app_workhistory", data_dic=history_dic)
                    print("..........7898u87")

                    # 파이썬 파일 이름 변경
                    sql.conn.commit()
                    os.rename(file_org_name, file_trans_name)
            sql.close()
            print("작업 끝!")
            # return HttpResponse({'success' : True}, status = 200)
        messages.info(request, dbinfo.message["mes_work_inserted"])
        return redirect("admin_index")

    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!__________________error!!!!______________!!!!!!!!!!!!!!!!!!!!!! ", e)
        print(e)
        # return HttpResponse({'success' : False}, status = 200)
        messages.info(request, dbinfo.message["mes_error"])
        sql.close()
        return redirect("admin_index")





'''
** END :  ------------------------ 관리자 페이지 Module -------------------------------
'''
