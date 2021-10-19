# -*- coding: utf-8 -*-

from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import query
## auth Check import

from .sqlMethod import sqlMethod
from django.contrib.auth.hashers import check_password
from django.conf import settings
## Password Check import
from PIL import Image

import json, base64, bson

from ..models import *
from datetime import datetime
from ast import literal_eval
from io import StringIO

from django.db import connection
from db_info import dbinfo

from ..Controller.UserAdapter import *
import psycopg2


class getTaskInfo:

    def __init__(self):

        self.res_dic = {}

    ## WorkRecord 테이블에서 작업 정보를 가져오는 로직
    def get_task_record(self, request):
        sqlMethodClsss = sqlMethod()

        get_user_name = UserAdapter().get_profile(request)

        try:
            column_list = [
<<<<<<< .mine
                            "work_id",
                            "work_type",
                            "work_status",
                            "reg_date",
                            "(select code_nm  from django_app_code_mst where code_id = work_status)  work_status_nm",
                            "(select code_nm  from django_app_code_mst where code_id = work_type) work_type_nm",
                            "(select memo from django_app_workhistory i where i.work_id= w.work_id and i.history_id = (select max(history_id) from django_app_workhistory h where h.work_id= w.work_id  ) ) memo" ,
                          ]
            work_list = sqlMethodClsss.select_workList(table_name="django_app_worklist w ", data_dic ={"worker_id":get_user_name}, status_list ={dbinfo.status['status_1cha_inspect_deagi'],dbinfo.status['status_complet'], dbinfo.status['status_manage_return'], dbinfo.status['status_1cha_companion_return'],dbinfo.status['status_1cha_man_companion_return']},column_list= column_list)
||||||| .r259
                            "work_id",
                            "work_type",
                            "work_status",
                            "reg_date",
                            "(select code_nm  from django_app_code_mst where code_id = work_status)  work_status_nm",
                            "(select code_nm  from django_app_code_mst where code_id = work_type) work_type_nm",
                            "(select memo from django_app_workhistory i where i.work_id= w.work_id and i.history_id = (select max(history_id) from django_app_workhistory h where h.work_id= w.work_id  ) ) memo" ,
                          ]
            work_list = sqlMethodClsss.select_workList(table_name="django_app_worklist w ", data_dic ={"worker_id":get_user_name}, status_list ={"C","I","R0", "R1","R5"},column_list= column_list)
=======
                "work_id",
                "work_type",
                "work_status",
                "reg_date",
                "(select code_nm  from django_app_code_mst where code_id = work_status)  work_status_nm",
                "(select code_nm  from django_app_code_mst where code_id = work_type) work_type_nm",
                "(select memo from django_app_workhistory i where i.work_id= w.work_id and i.history_id = (select max(history_id) from django_app_workhistory h where h.work_id= w.work_id  ) ) memo",
            ]
            work_list = sqlMethodClsss.select_workList(table_name="django_app_worklist w ",
                                                       data_dic={"worker_id": get_user_name},
                                                       status_list={dbinfo.status['status_1cha_inspect_deagi'],
                                                                    dbinfo.status['status_complet'],
                                                                    dbinfo.status['status_manage_return'],
                                                                    dbinfo.status['status_1cha_companion_return'],
                                                                    dbinfo.status['status_1cha_man_companion_return']},
                                                       column_list=column_list)
>>>>>>> .r284
            print(work_list)
        except:
            raise

        column_list = [
<<<<<<< .mine
                        "work_id",
                        "work_type",
                        "work_status",
                        "reg_date",
                        "(select code_nm  from django_app_code_mst where code_id = work_status)  work_status_nm",
                        "(select code_nm  from django_app_code_mst where code_id = work_type) work_type_nm",
                        "(select memo from django_app_workhistory i where i.work_id= w.work_id and i.history_id = (select max(history_id) from django_app_workhistory h where h.work_id= w.work_id  ) ) memo",
                        "(select case when min(daw.work_status) = '"+dbinfo.status['status_1cha_inspect_run']+"' then '1차 검수 진행' when min(daw.work_status) = '"+dbinfo.status['status_2cha_inspect_run']+"' then '2차 검수 진행' when min(daw.work_status) = '"+dbinfo.status['status_3cha_inspect_run']+"' then '3차 검수 진행' END AS my_status from django_app_workhistory daw where daw.reg_id = '"+get_user_name+"' and daw.work_id = w.work_id)",
                        "(select max(daw.reg_date) my_regDate from django_app_workhistory daw where daw.reg_id = '"+get_user_name+"' and daw.work_id = w.work_id)"
                      ]
        option = "and ((select min(work_status) from django_app_workhistory where reg_id = 'test02' and work_id = w.work_id ) = '"+dbinfo.status['status_1cha_inspect_run']+"'" +\
                "or (select min(work_status) from django_app_workhistory where reg_id = 'test02' and work_id = w.work_id ) = '"+dbinfo.status['status_2cha_inspect_run']+"'" +\
                "or (select min(work_status) from django_app_workhistory where reg_id = 'test02' and work_id = w.work_id ) = '"+dbinfo.status['status_3cha_inspect_run']+"')" +\
                "group by w.work_id"
||||||| .r259
                        "work_id",
                        "work_type",
                        "work_status",
                        "reg_date",
                        "(select code_nm  from django_app_code_mst where code_id = work_status)  work_status_nm",
                        "(select code_nm  from django_app_code_mst where code_id = work_type) work_type_nm",
                        "(select memo from django_app_workhistory i where i.work_id= w.work_id and i.history_id = (select max(history_id) from django_app_workhistory h where h.work_id= w.work_id  ) ) memo",
                        "(select case when min(daw.work_status) = 'D' then '1차 검수 진행' when min(daw.work_status) = 'F' then '2차 검수 진행' when min(daw.work_status) = 'H' then '3차 검수 진행' END AS my_status from django_app_workhistory daw where daw.reg_id = '"+get_user_name+"' and daw.work_id = w.work_id)",
                        "(select max(daw.reg_date) my_regDate from django_app_workhistory daw where daw.reg_id = '"+get_user_name+"' and daw.work_id = w.work_id)"
                      ]
        option = "and ((select min(work_status) from django_app_workhistory where reg_id = 'test02' and work_id = w.work_id ) = 'D'" +\
                "or (select min(work_status) from django_app_workhistory where reg_id = 'test02' and work_id = w.work_id ) = 'F'" +\
                "or (select min(work_status) from django_app_workhistory where reg_id = 'test02' and work_id = w.work_id ) = 'H')" +\
                "group by w.work_id"
=======
            "work_id",
            "work_type",
            "work_status",
            "reg_date",
            "(select code_nm  from django_app_code_mst where code_id = work_status)  work_status_nm",
            "(select code_nm  from django_app_code_mst where code_id = work_type) work_type_nm",
            "(select memo from django_app_workhistory i where i.work_id= w.work_id and i.history_id = (select max(history_id) from django_app_workhistory h where h.work_id= w.work_id  ) ) memo",
            "(select case when min(daw.work_status) = '" + dbinfo.status[
                'status_1cha_inspect_run'] + "' then '1차 검수 진행' when min(daw.work_status) = '" + dbinfo.status[
                'status_2cha_inspect_run'] + "' then '2차 검수 진행' when min(daw.work_status) = '" + dbinfo.status[
                'status_3cha_inspect_run'] + "' then '3차 검수 진행' END AS my_status from django_app_workhistory daw where daw.reg_id = '" + get_user_name + "' and daw.work_id = w.work_id)",
            "(select max(daw.reg_date) my_regDate from django_app_workhistory daw where daw.reg_id = '" + get_user_name + "' and daw.work_id = w.work_id)"
        ]
        option = "and ((select min(work_status) from django_app_workhistory where reg_id = 'test02' and work_id = w.work_id ) = '" + \
                 dbinfo.status['status_1cha_inspect_run'] + "'" + \
                 "or (select min(work_status) from django_app_workhistory where reg_id = 'test02' and work_id = w.work_id ) = '" + \
                 dbinfo.status['status_2cha_inspect_run'] + "'" + \
                 "or (select min(work_status) from django_app_workhistory where reg_id = 'test02' and work_id = w.work_id ) = '" + \
                 dbinfo.status['status_3cha_inspect_run'] + "')" + \
                 "group by w.work_id"
>>>>>>> .r284

        inspect_list = sqlMethodClsss.select_workList(table_name="django_app_worklist w ", data_dic={},
                                                      status_list={"I"}, column_list=column_list, option=option)
        print(inspect_list)

        sqlMethodClsss.close()

        return work_list, inspect_list

    ## WorkRecord 테이블에서 작업 정보를 가져오는 로직
    def get_task_record_bak(self, request):

        print("get_task_record")

        ## 반려 메시지는 반려일 경우에만 해당하므로 조합할 리스트 길이에 맞춰서 재조합
        deny_message_list = []

        try:
            task_add_history = WorkRecord.objects.filter(work_category='T', reg_id=request.user)
            task_complete_history = WorkRecord.objects.filter(work_category='Q', reg_id=request.user)
            task_cancel_history = WorkRecord.objects.filter(work_category='K', reg_id=request.user)
            admin_cancel_history = WorkRecord.objects.filter(work_category="N", reg_id=request.user)
            admin_approve_history = WorkRecord.objects.filter(work_category="Y", reg_id=request.user)
        except:
            raise

        for item in task_add_history:
            deny_message = "None"
            deny_message_list.append(deny_message)

        for item in task_complete_history:
            deny_message = "None"
            deny_message_list.append(deny_message)

        for item in task_cancel_history:
            deny_message = "None"
            deny_message_list.append(deny_message)

        ## cancel일 경우에 반려 메시지가 존재하므로 메시지는 따로 리스트 append 처리
        for item in admin_cancel_history:

            query_check = admin_cancel_history = WorkRecord.objects.filter(work_category='N', reg_id=request.user)

            if query_check.exists():

                record_check = WorkRecord.objects.filter(work_category='T', reg_id=request.user)

                for item in record_check:

                    deny_check = DenyReason.objects.filter(record_num_id=item.id)

                    if deny_check.exists():

                        get_deny_message = DenyReason.objects.filter(record_num_id=item.id)

                        for item in get_deny_message:
                            deny_message_list.append(str(item.reason_data_field))

        for item in admin_approve_history:
            deny_message = "None"
            deny_message_list.append(deny_message)

        task_add_history = list(task_add_history)
        task_complete_history = list(task_complete_history)
        task_cancel_history = list(task_cancel_history)
        admin_cancel_history = list(admin_cancel_history)
        admin_approve_history = list(admin_approve_history)

        task_add_history += task_complete_history
        task_add_history += task_cancel_history
        task_add_history += admin_cancel_history
        task_add_history += admin_approve_history

        inspect_add_history = WorkRecord.objects.filter(work_category='I', reg_id=request.user)
        inspect_complete_history = WorkRecord.objects.filter(work_category='U', reg_id=request.user)
        inspect_cancel_history = WorkRecord.objects.filter(work_category='H', reg_id=request.user)

        inspect_add_history = list(inspect_add_history)
        inspect_complete_history = list(inspect_complete_history)
        inspect_cancel_history = list(inspect_cancel_history)

        inspect_add_history += inspect_complete_history
        inspect_add_history += inspect_cancel_history

        # return zip(range(1, len(my_assigned_task) + 1), my_assigned_task, my_task_list, my_reward)

        ## 반려 메시지는 작업에만 존재하므로 zip으로 따로 작업 부분만 묶어서 처리함

        return zip(task_add_history, deny_message_list), inspect_add_history

        ## DB 정보 체크

    def check_db_data(self, request, user_name, task_num):

        try:
            print("Check DB Data")

            def return_string(*argument):

                trans_data = bytes(*argument, 'utf8')
                trans_data = trans_data.decode('utf-8')

                return trans_data

            # ajax로 받은 데이터를 체크

            get_json_data = json.loads(request.body)

            # print("Get Json Data : ",get_json_data)

            condition_check = WorkRecord.objects.filter(task_num=task_num, work_category="Q")

            ## 검수 신청에 해당하므로 검수 데이터 구성 로직 활성화
            if condition_check.exists():

                user_name = request.user

                print(" Inspect Data Check Detect ")

                get_record = WorkRecord.objects.get(reg_id=user_name, work_category="I", task_num=task_num,
                                                    worklist_task_num_id=get_json_data)
                record_unique_key = get_record.id

                get_tasklist = InspectHistory.objects.filter(work_num_id=record_unique_key).order_by(
                    'inspect_image_num')

                get_id_list, get_width_list, get_height_list = [], [], []
                get_scaleX_list, get_scaleY_list, get_name_list = [], [], []
                get_images_list, get_path_list, get_type_list, get_length_list = [], [], [], []

                for item in get_tasklist:
                    task_data = bytes(item.inspect_data)
                    task_data = bson.loads(task_data)

                    data_id = return_string(task_data['id'])
                    get_id_list.append(data_id)

                    data_width = task_data['width']
                    get_width_list.append(data_width)

                    data_height = task_data['height']
                    get_height_list.append(data_height)

                    data_scaleX = task_data['scaleX']
                    get_scaleX_list.append(data_scaleX)

                    data_scaleY = task_data['scaleY']
                    get_scaleY_list.append(data_scaleY)

                    data_name = return_string(task_data['name'])
                    get_name_list.append(data_name)

                    data_images = str(task_data['images'])

                    get_images_list.append(data_images)

                    # print("Inspect Label Check : ", data_images)

                    data_path = return_string(task_data['path'])
                    get_path_list.append(data_path)

                    data_length = task_data['length']
                    get_length_list.append(data_length)

                    data_type = return_string(task_data['type'])
                    get_type_list.append(data_type)

                # get_images_list = str(get_images_list)
                # recombine_dict = {"id": get_id_list[item], "width": get_width_list[item], "height" : get_height_list[item], "scaleY": get_scaleY_list[item], "scaleX":get_scaleX_list[item], "name":get_name_list[item], "images": "[" + "]", "length":get_length_list[item], "path":get_path_list[item], "type":get_type_list[item]}

                print("*********** || Dict Combine Data Check || *************")

                # print("ID : ",get_id_list[0])
                # print("Width : ",get_width_list[0])
                # print("height : ",get_height_list[0])
                # print("scaleX : ",get_scaleX_list[0])
                # print("scaleY : ",get_scaleY_list[0])
                # print("name : ", get_name_list[0])

                # # print(get_images_list[0])
                # print("path : ", get_path_list[0])
                # print("length : ", get_length_list[0])
                # # print(len(get_images_list))

                recombine_dict = {"id": get_id_list[0], "width": get_width_list[0], "height": get_height_list[0],
                                  "scaleX": get_scaleX_list[0], "scaleY": get_scaleY_list[0], "name": get_name_list[0],
                                  "images": "[" + "]", "length": get_length_list[0], "path": get_path_list[0],
                                  "type": get_type_list[0]}
                # recombine_dict = {"id": get_id_list[0], "width": get_width_list[0], "height" : get_height_list[0], "scaleY": get_scaleY_list[0], "scaleX":get_scaleX_list[0], "name":get_name_list[0], "images": "[" + "]", "labels": "[" + "]", "length":get_length_list[0], "path":get_path_list[0], "type":get_type_list[0]}

                # recombine_dict = recombine_dict.replace("\\","")

                return recombine_dict, get_images_list


            ## 재작업에 해당하므로 재작업 데이터 구성 로직 활성화
            else:

                print(" Task Data Check Detect ")

                get_record = WorkRecord.objects.get(reg_id=user_name, work_category="T", task_num=task_num,
                                                    worklist_task_num_id=get_json_data)

                record_key_2 = get_record.id

                get_tasklist = TaskHistory.objects.filter(work_num_id=record_key_2).order_by('task_image_num')

                get_id_list, get_width_list, get_height_list = [], [], []
                get_scaleX_list, get_scaleY_list, get_name_list = [], [], []
                get_images_list, get_path_list, get_type_list, get_length_list = [], [], [], []

                for item in get_tasklist:
                    task_data = bytes(item.task_data)
                    task_data = bson.loads(task_data)

                    data_id = return_string(task_data['id'])
                    get_id_list.append(data_id)

                    data_width = task_data['width']
                    get_width_list.append(data_width)

                    data_height = task_data['height']
                    get_height_list.append(data_height)

                    data_scaleX = task_data['scaleX']
                    get_scaleX_list.append(data_scaleX)

                    data_scaleY = task_data['scaleY']
                    get_scaleY_list.append(data_scaleY)

                    data_name = return_string(task_data['name'])
                    get_name_list.append(data_name)

                    data_images = str(task_data['images'])

                    get_images_list.append(data_images)

                    print("Task Label Check : ", data_images)

                    data_path = return_string(task_data['path'])
                    get_path_list.append(data_path)

                    data_length = task_data['length']
                    get_length_list.append(data_length)

                    data_type = return_string(task_data['type'])
                    get_type_list.append(data_type)

                print("*********** || Dict Combine Data Check || *************")

                # print("ID : ",get_id_list[0])
                # print("Width : ",get_width_list[0])
                # print("height : ",get_height_list[0])
                # print("scaleX : ",get_scaleX_list[0])
                # print("scaleY : ",get_scaleY_list[0])
                # print("name : ", get_name_list[0])

                # # print(get_images_list[0])
                # print("path : ", get_path_list[0])
                # print("length : ", get_length_list[0])
                # # print(len(get_images_list))

                recombine_dict = {}

                if get_tasklist:
                    recombine_dict = {"id": get_id_list[0], "width": get_width_list[0], "height": get_height_list[0],
                                      "scaleX": get_scaleX_list[0], "scaleY": get_scaleY_list[0],
                                      "name": get_name_list[0],
                                      "images": "[" + "]", "length": get_length_list[0], "path": get_path_list[0],
                                      "type": get_type_list[0]}
                # recombine_dict = {"id": get_id_list[0], "width": get_width_list[0], "height" : get_height_list[0], "scaleY": get_scaleY_list[0], "scaleX":get_scaleX_list[0], "name":get_name_list[0], "images": "[" + "]", "labels": "[" + "]", "length":get_length_list[0], "path":get_path_list[0], "type":get_type_list[0]}

                # recombine_dict = recombine_dict.replace("\\","")

                return recombine_dict, get_images_list
        except:
            raise

    ## 작업 페이지에서 번호 이동 할때마다 ajax로 데이터를 받아서 저장하는 로직
    # 저작도구에서 label info save 버튼을 누를 경우 ajax로 데이터를 받아서 db 저장하는 것으로 사용
    def get_task_db_insert(self, request, user_name, task_num):

        # print('-----------------------------------------------')
        # # print(request.body)
        # # print(str(user_name))
        # #query_set = WorkRecord.objects.all()
        query_set = sqlMethod()

        # print("작업, 검수에서 번호를 이동할 때 동작하는 저장 로직")

        # ## 검수 신청 기록이 있는지
        # #inspect_record_check = WorkRecord.objects.filter(work_status = 'D', work_id = task_num)
        # inspect_record_check = []

        # data_dic = {"work_id": task_num , "work_status" : "C"}
        # get_workhistory_info = query_set.select_workList(table_name="django_app_workhistory",data_dic=data_dic)

        # ## 작업 신청 기록이 있는지
        # task_record_check = WorkRecord.objects.filter(work_category = 'AA', task_num = task_num)
        # table_name = 'django_app_workhistory'
        # data_dic = {'work_status':'B',}
        # task_record_check = query_set.select_workList(table_name=table_name,data_dic=data_dic)

        # query_set.conn.commit()

        # ## 검수 신청 기록이 있는 경우
        # if len(inspect_record_check) > 0:

        #     print("Inspect Save Data")
        #     data_dic = {"work_id": str(task_num) , "work_status" : "I", "reg_id" : str(user_name)}

        #     get_record_info = query_set.select_workList(table_name="django_app_workhistory",data_dic=data_dic)

        #     #get_record_info = query_set.select_workList(work_status = 'I', work_id = task_num, reg_id = user_name)

        # get_json_data = json.loads(request.body.decode('utf-8'))
        # parsing_data = json.loads(request.body)
        # get_json_data = bson.dumps(get_json_data)

        # #workrecord_key = get_record_info.get("history_id")
        # print("get_record_info----------------------------------------------")
        # print(get_record_info)
        # workrecord_key = get_record_info[0].get("history_id")

        # json_parser = parsing_data.get('images')

        # for item in json_parser:

        #     ## Dict Get Image Number
        #     image_number = item.get('id')

        # # image_number = json_parser.get('id')

        # image_number = image_number.split('-')[1]

        # worklist = WorkList.objects.get(task_num = workrecord_key)

        # worklist_save_path = worklist.image_save_path

        # inspect_history = InspectHistory()

        # workrecord_primary_id = get_record_info.id

        # # 저장 하기 이전에 Update 할지 Insert 할지 확인하기 위해서 Query를 돌려서 확인
        # inspect_history_query = InspectHistory.objects.filter(inspect_image_num = image_number, inspector_id = user_name, work_num_id = workrecord_primary_id)

        # ## DB Query Check 분기점, 존재할 경우 Update, 존재하지 않을 경우 Insert 수행
        # if inspect_history_query.exists():

        #     inspect_info = InspectHistory.objects.get(inspect_image_num = image_number, inspector_id = user_name, work_num_id = workrecord_primary_id)
        #     current_time = datetime.now()

        #         print("INSPECT(DB) UPDATE EVENT")

        #         inspect_info.inspect_data = get_json_data
        #         inspect_info.reg_date = current_time
        #         inspect_info.save()

        # #task_record_check = WorkRecord.objects.filter(work_category = 'AA', task_num = task_num)

        # data_dic = {"work_id": task_num , "work_status" : "B"}
        # get_workhistory_B_info = query_set.select_workList(table_name="django_app_workhistory",data_dic=data_dic)

        # data_dic = {"work_id": task_num , "work_status" : "D"}
        # get_workhistory_D_info = query_set.select_workList(table_name="django_app_workhistory",data_dic=data_dic)

        # query_set.conn.commit()
        # ## 작업 신청 기록이 있는 경우
        # if len(get_workhistory_B_info)>0:

        #     ## 작업 관련 로직이 검수 관련 로직 이후 동작하므로 조건문으로 검수 관련 로직에서 동작할 수 없도록 처리
        #     if len(get_workhistory_D_info) >0:
        #         print("작업에 해당하므로 로직 정지")

        #     else :
        #         ## 작업 정보를 저장하는 로직
        #         print("Task Save Data")

        # get_record_info = query_set.filter(work_category = 'AA', task_num = task_num, reg_id = user_name).order_by('-reg_date').first()

        # print(get_record_info)
        ## 한글이 깨짐
        # get_json_data = json.loads(request.body.decode('utf-8-sig'))

        # parsing_data = json.loads(request.body)
        # get_json_data = json.dumps(get_json_data, ensure_ascii=False)

        get_json_data = json.loads(request.body.decode('utf-8-sig'))
        parsing_data = json.loads(request.body)
        get_json_data = json.dumps(get_json_data, ensure_ascii=False)

        # workrecord_key = get_record_info.worklist_task_num_id

        # startTime = parsing_data.get('start')
        # endTime = parsing_data.get('end')
        # task_id = parsing_data.get('attributes')

        startTime = parsing_data.get('start')
        endTime = parsing_data.get('end')
        task_id = parsing_data.get('attributes')
        group_id = parsing_data.get('group')

        # # for item in json_parser:

        # #     ## Dict Get Image Number
        # #     image_number = item.get('id')

        # # image_number = json_parser.get('id')

        # # image_number = image_number.split('-')[1]

        # # worklist = WorkList.objects.get(task_num = workrecord_key)
        # # worklist = WorkList.objects.get(task_num = task_num)
        # sqlMethodClsss = sqlMethod()
        # data_dic = {"work_id": task_num}
        # worklist = sqlMethodClsss.select_workList(table_name="django_app_worklist", data_dic=data_dic)
        # print("@@@@@@@@@@@@@@@worklist", worklist)
        # worklist_save_path = worklist.video_path

        # worklist_save_path = worklist[0].get("video_path")

        # query_set.conn.commit()

        # # task_history = TaskHistory()

        # # workrecord_primary_id = get_record_info.id

        # ## taskhitory_query를 통해서 해당 번호의 작업이 존재하는지 존재하지 않는지 체크하는 쿼리
        # # taskhistory_query = TaskHistory.objects.filter(start_time = startTime, end_time = endTime, tasker_id = user_name, work_num_id = workrecord_primary_id)
        # """ try:
        #     taskhistory_query = TaskHistory.objects.get(start_time = startTime, end_time = endTime, tasker_id = user_name, work_num_id = task_num)
        #     print("--------------------------------------------------------", taskhistory_query)
        # ## DB Query 작업 분기점, 존재할 경우 Update, 존재하지 않을 경우 Insert 수행
        # ## DB Update Data
        # # if taskhistory_query.exists():

        #     # task_info = TaskHistory.objects.get(start_time = startTime, end_time = endTime, tasker_id = user_name, work_num_id = workrecord_primary_id)
        #     # task_info = TaskHistory.objects.get(start_time = startTime, end_time = endTime, tasker_id = user_name, work_num_id = task_num)
        #     current_time = datetime.now()

        #     print("Task(DB) UPDATE EVENT")

        #     # task_info.task_data = get_json_data
        #     # task_info.reg_date = current_time
        #     # task_info.save()
        #     taskhistory_query.task_data = get_json_data
        #     taskhistory_query.reg_date = current_time
        #     taskhistory_query.save()
        # ## DB Insert Data
        # except Exception as e:
        # # else:
        #     print(e);
        #     print("Task(DB) INSERT EVENT")
        #     # print(workrecord_primary_id)
        #     # task_history.task_id = workrecord_primary_id

        #     task_history.work_fold_path = worklist_save_path

        #     task_history.task_data = get_json_data

        #     task_history.task_image_num = 0

        #     task_history.tasker_id = str(user_name)

        #     # task_history.work_num_id = workrecord_key
        #     task_history.work_num_id = task_num

        #     task_history.reg_date = datetime.now()

        #     ## JSON에서 값꺼내기
        #     task_history.end_time = startTime

        #     task_history.start_time = endTime

        #     task_history.save() """
        # print("-------------------insert 시작-----------------------------")
        # conn = psycopg2.connect(dbinfo.conn_info)
        # print("-------------------db 커넥션 완료---------------------------")
        # cursor = conn.cursor()
        # user_name = str(user_name)
        # current_time = datetime.now()

        print("-------------------insert 시작-----------------------------")
        conn = psycopg2.connect(dbinfo.conn_info)
        print("-------------------db 커넥션 완료---------------------------")
        cursor = conn.cursor()
        user_name = str(user_name)
        # current_time = datetime.now()

        # value = [task_id, worklist_save_path, get_json_data, user_name, current_time, task_num, '0', endTime, startTime]
        # print(value)
        # print(task_id)
        # strValue = "','".join(value)
        # try :
        #     _sql =  "insert into django_app_tasklist " + \
        #             "( task_id, associated_video_path, task_data, work_id, end_time," + \
        #             "reg_id, reg_date, start_time)" + \
        #             "values (" + \
        #             "'" + str(task_id) + "'," +\
        #             "'" + worklist_save_path + "'," +\
        #             "'" + get_json_data + "'," + \
        #             "'" + task_num + "'," + \
        #             "'" + endTime + "'," + \
        #             "'" + user_name + "'," + \
        #             " now()," +\
        #             "'" + startTime + "'" + \
        #             ")" + \
        #             " on conflict (work_id, task_id) DO " + \
        #             "update set task_data = '" + get_json_data + "'," + \
        #             "reg_date = now()," + \
        #             "end_time = '" + endTime + "'," + \
        #             "start_time = '" + startTime + "';"
        #     print(_sql)
        #     cursor.execute(_sql)
        # except :
        #     conn.rollback()

        # conn.commit()
        # conn.close()
        print("_______________________________________________________!")
        print(task_id)
        print("_______________________________________________________!")
        print(task_num)
        print("_______________________________________________________!")
        print(endTime)
        print("_______________________________________________________!")
        print(user_name)
        print("_______________________________________________________!")
        print(startTime)
        print("_______________________________________________________!")
        print(group_id)
        print("_______________________________________________________!")

        try:
            _sql = "insert into django_app_tasklist " + \
                   "( task_id, associated_video_path, task_data, work_id, end_time," + \
                   "reg_id, reg_date, start_time, group_id)" + \
                   "values (" + \
                   "'" + str(task_id) + "'," + \
                   "''," + \
                   "'" + get_json_data + "'," + \
                   "'" + task_num + "'," + \
                   "'" + str(endTime) + "'," + \
                   "'" + user_name + "'," + \
                   " now()," + \
                   "'" + str(startTime) + "'," + \
                   "'" + group_id + "'" + \
                   ")" + \
                   " on conflict (work_id, task_id) DO " + \
                   "update set task_data = '" + get_json_data + "'," + \
                   "reg_date = now()," + \
                   "end_time = '" + str(endTime) + "'," + \
                   "start_time = '" + str(startTime) + "'," + \
                   "reject_status = 'N' ;"
            print(_sql)
            cursor.execute(_sql)
        except Exception as e:
            conn.rollback()
            print(
                "--------------------------------------------------error---------------------------------------------------")
            raise
            print(e)

        conn.commit()
        conn.close()

    # 저작도구에서 region delete를 하면 db taskhistory instance 삭제
    def task_db_delete(self, request, user_name, task_num):
        parsing_data = json.loads(request.body)
        startTime = parsing_data.get('start')
        endTime = parsing_data.get('end')
        print("---------------------------------------------------------------")
        print("Delete Region : start_time : " + str(startTime) + ", end_time : " + str(endTime) + ", reg_id : " + str(
            user_name) + ", work_id : " + str(task_num))
        print("---------------------------------------------------------------")

        sql_query = sqlMethod()
        data_dic = {
            "start_time": str(startTime),
            "end_time": str(endTime),
            "reg_id": str(user_name),
            "work_id": str(task_num)
        }
        try:
            instance = sql_query.delete(table_name="django_app_tasklist", data_dic=data_dic, option=None)
            sql_query.close()
        except Exception as e:
            print("____________________________Delete__error!!!!!!!!____________________")
            print(e)
            sql_query.close()
            raise

    # 이상행동 저작도구에서 region delete를 하면 db taskhistory instance 삭제
    def task_db_delete_abnormal(self, request, user_name, task_num):
        parsing_data = json.loads(request.body)
        startTime = parsing_data.get('start')
        endTime = parsing_data.get('end')
        TaskIdList = parsing_data.get('chgTaskIdList')
        removeTaskId = parsing_data.get('task_id')
        sql_query = sqlMethod()
        try:
            print("---------------------------------------------------------------")
            print(
                "Delete Region : start_time : " + str(startTime) + ", end_time : " + str(endTime) + ", reg_id : " + str(
                    user_name) + ", work_id : " + str(task_num))
            print("---------------------------------------------------------------")

            data_dic = {
                "start_time": str(startTime),
                "end_time": str(endTime),
                "reg_id": str(user_name),
                "work_id": str(task_num)
            }
            delete_region = sql_query.delete(table_name="django_app_tasklist", data_dic=data_dic, option=None)
            for task_id in TaskIdList:
                tmpId = task_id - 1
                update_dic = {
                    'task_id': str(tmpId)
                }
                con_dic = {
                    'task_id': str(task_id),
                    'work_id': str(task_num)
                }
                update_region = sql_query.update_status(table_name="django_app_tasklist", data_dic=update_dic,
                                                        con_dic=con_dic)
            sql_query.close()
        except Exception as e:
            print("____________________________Delete__error!!!!!!!!____________________")
            print(e)
            sql_query.close()
            raise

    # 작업을 시작하면 task_num, user_name 해당하는 taskhistory 모두 select
    def task_db_select_all(self, user_name, task_num):
        try:
            sql_query = sqlMethod()
            data_dic = {
                "work_id": task_num,
            }
            column_list = {"task_data"}
            option = " order by start_time"
            instance = sql_query.select_workList(table_name="django_app_tasklist", data_dic=data_dic,
                                                 column_list=column_list, option=option)
            # instance = TaskHistory.objects.filter(work_num_id = task_num).values('task_data').order_by('start_time')
            # print("instance--------------------------------------------------")
            # print(instance)

            sql_query.close()
            task_data_list = []
            for i in range(len(instance)):
                # print(instance[i]['task_data'])
                task_data_list.append(instance[i]['task_data'])

            return task_data_list
        except:
            raise

    def task_db_select_all2(self, work_id):
        try:
            sql_query = sqlMethod()
            data_dic = {
                "work_id": work_id,
            }
            column_list = {"task_data"}
            option = " order by start_time"
            instance = sql_query.select_workList(table_name="django_app_tasklist", data_dic=data_dic,
                                                 column_list=column_list, option=option)
            # instance = TaskHistory.objects.filter(work_num_id = task_num).values('task_data').order_by('start_time')
            # print("instance--------------------------------------------------")
            # print(instance)

            sql_query.close()
            task_data_list = []
            for i in range(len(instance)):
                # print(instance[i]['task_data'])
                task_data_list.append(instance[i]['task_data'])

            return task_data_list
        except:
            raise

    # 이상행동 작업 파일 업로드 시 db 작업 이력 조회
    def task_db_select(self, user_name, task_num):

        # task_data =  list(TaskHistory.objects.filter(work_num_id = task_num).values('task_id', 'task_data').order_by('task_id'))
        sql_query = sqlMethod()
        column_list = {"task_data", "task_id", "reject_status"}
        data_dic = {
            "work_id": task_num
            # "reg_id": user_name
        }
        option = "order by start_time"
        try:
            task_data = sql_query.select_workList(table_name="django_app_tasklist", data_dic=data_dic,
                                                  column_list=column_list, option=option)
        except:
            raise
        sql_query.close()

        print("task_data : ", task_data)

        return task_data

    def get_memo(self, task_num):
        try:
            sql_query = sqlMethod()
            column_list = {'memo', 'history_id'}
            data_dic = {
                "work_id": task_num
            }
            option = 'order by history_id desc limit 1'
            memo = sql_query.select_workList(table_name="django_app_workhistory", data_dic=data_dic,
                                             column_list=column_list, option=option, status_list=None)
            sql_query.close()

            return memo
        except:
            raise

    # #가장 최신의 memo 데이터 가져오기
    # def history_db_latest_memo(self, task_num):
    #     sql_query = sqlMethod()
    #     data_dic = {
    #         "work_id" : task_num,
    #     }
    #     column_list = {"memo"}
    #     option = "order by reg_date"
    #     history_memo = sql_query.select_workList(table_name="django_app_workhistory", data_dic=data_dic, column_list=column_list,option=option)
    #     # instance = TaskHistory.objects.filter(work_num_id = task_num).values('task_data').order_by('start_time')
    #     #print("instance--------------------------------------------------")
    #     # print(instance)
    #
    #     sql_query.close()
    #     return history_memo
