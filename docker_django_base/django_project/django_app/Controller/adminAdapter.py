from django.contrib import auth
from django.contrib.auth.models import User
## auth Check import

from django.contrib.auth.hashers import check_password
## Password Check import
from ..models import *
from datetime import datetime

from .sqlMethod import sqlMethod
import json, bson
from db_info import dbinfo



class adminAdapter():

    def __init__(self):
        
        self.res_dic = {}

    ## 관리자 페이지에서 입력된 반려 메시지를 가져와서 DenyReason 테이블에 저장하는 로직
    def task_deny_message_insert(self, request, record_key, refuse_message) : 

        #print("반려 메시지 GET", refuse_message)
        #print("record_key : ", record_key)

        deny_table = DenyReason()
        record = WorkRecord.objects.get(worklist_task_num_id = record_key, work_category ='T')
    
        deny_table.record_num_id = record.id

        deny_table.task_num = str(record.task_num)
        deny_table.reason_data_field = str(refuse_message)
        deny_table.task_type = 'TK'
        deny_table.reg_id = str(request.user)
        deny_table.reg_date = datetime.now()

        deny_table.save()

        return True

    
    ## 전체 유저 정보 GET
    def getUserList(self, request):

        sql_query=sqlMethod()
        try:
            user_list = sql_query.select_workList(table_name="django_app_profile", data_dic={'1':'1'})

            # user_list = Profile.objects.all()

            # print(user_list)
            sql_query.close()
        except:
            raise
        return user_list

    ## 그룹 유저 정보 GET
    def getGroupUserList(self, request, group):

        sql_query=sqlMethod()

        user_list = sql_query.select_workList(table_name="django_app_profile", data_dic={'group_id':str(group)})

        # user_list = Profile.objects.all()

        # print(user_list)
        sql_query.close()
        return user_list


    ## 프로젝트 진행 현황 계산 로직
    def getProjectProgress(self, request):

        sql_query = sqlMethod()

        # # 전체 작업
        # total_worklist = WorkList.objects.all()
        # total_worklist_len = len(total_worklist)
        try:
            total_worklist = sql_query.select_workList(table_name="django_app_worklist", data_dic={'1':'1'})
            total_worklist_len = len(total_worklist)
        except:
            raise

        # print(total_worklist_len)

        # # 작업 대기
        # task_ready_list = WorkList.objects.filter(work_status = 'A')
        # task_ready_len = len(task_ready_list)
        try:
            task_ready_list = sql_query.select_workList(table_name="django_app_worklist", data_dic={'work_status':dbinfo.status['status_work_deagi']})
            task_ready_len = len(task_ready_list)
        except:
            raise

        # # 작업 중 작업
        # task_working_list = WorkList.objects.filter(work_status = 'B')
        # task_working_len = len(task_working_list)
        try:
            task_working_list = sql_query.select_workList(table_name="django_app_worklist", data_dic={'work_status':dbinfo.status['status_work_run']})
            task_working_len = len(task_working_list)
        except:
            raise

        # # 작업 완료 작업
        # inspect1_ready_list = WorkList.objects.filter(work_status = 'C')
        # inspect1_ready_len = len(inspect1_ready_list)
        try:
            inspect1_ready_list = sql_query.select_workList(table_name="django_app_worklist", data_dic={'work_status':dbinfo.status['status_1cha_inspect_deagi']})
            inspect1_ready_len = len(inspect1_ready_list)
        except:
            raise

        # inspect1_working_list = WorkList.objects.filter(work_status = 'D')
        # inspect1_working_len = len(inspect1_working_list)
        try:
            inspect1_working_list = sql_query.select_workList(table_name="django_app_worklist", data_dic={'work_status':dbinfo.status['status_1cha_inspect_run']})
            inspect1_working_len = len(inspect1_working_list)
        except:
            raise

        # inspect2_ready_list = WorkList.objects.filter(work_status = 'E')
        # inspect2_ready_len = len(inspect2_ready_list)
        try:
            inspect2_ready_list = sql_query.select_workList(table_name="django_app_worklist", data_dic={'work_status':dbinfo.status['status_2cha_inspect_deagi']})
            inspect2_ready_len = len(inspect2_ready_list)
        except:
            raise

        # inspect2_working_list = WorkList.objects.filter(work_status = 'F')
        # inspect2_working_len = len(inspect2_working_list)
        try:
            inspect2_working_list = sql_query.select_workList(table_name="django_app_worklist", data_dic={'work_status':dbinfo.status['status_2cha_inspect_run']})
            inspect2_working_len = len(inspect2_working_list)
        except:
            raise

        # inspect3_ready_list = WorkList.objects.filter(work_status = 'G')
        # inspect3_ready_len = len(inspect3_ready_list)
        try:
            inspect3_ready_list = sql_query.select_workList(table_name="django_app_worklist", data_dic={'work_status':dbinfo.status['status_3cha_inspect_deagi']})
            inspect3_ready_len = len(inspect3_ready_list)
        except:
            raise

        # inspect3_working_list = WorkList.objects.filter(work_status = 'H')
        # inspect3_working_len = len(inspect3_working_list)
        try:
            inspect3_working_list = sql_query.select_workList(table_name="django_app_worklist", data_dic={'work_status':dbinfo.status['status_3cha_inspect_run']})
            inspect3_working_len = len(inspect3_working_list)
        except:
            raise

        # # 검수 완료 작업
        # task_complete_list = WorkList.filter(work_status = 'I')
        # task_complete_len = len(task_complete_list)
        try:
            task_complete_list = sql_query.select_workList(table_name="django_app_worklist", data_dic={'work_status':dbinfo.status['status_complet']})
            task_complete_len = len(task_complete_list)
        except:
            raise

        res_dic = {}
        res_dic['total_worklist_len'] = total_worklist_len
        res_dic['task_ready_len'] = task_ready_len
        res_dic['task_working_len'] = task_working_len
        res_dic['task_complete_len'] = task_complete_len
        res_dic['inspect1_ready_len'] = inspect1_ready_len
        res_dic['inspect1_working_len'] = inspect1_working_len
        res_dic['inspect2_ready_len'] = inspect2_ready_len
        res_dic['inspect2_working_len'] = inspect2_working_len
        res_dic['inspect3_ready_len'] = inspect3_ready_len
        res_dic['inspect3_working_len'] = inspect3_working_len

        # print(res_dic)
        sql_query.close()
        return res_dic

        # ## 작업이 완료된 기점으로 계산 
        # task_complete_list = WorkList.objects.filter(task_status = 'C')
        
        # ## 검수가 완료된 기점으로 계산 
        # inspect_complete_list = WorkList.objects.filter(inspect_status = 'C')

        # length_to_task = len(task_complete_list)
        # length_to_inspect = len(inspect_complete_list)

        # task_complete_process = length_to_task / worklist_len
        # inspect_complete_process = length_to_inspect / worklist_len

        # ## 프론트에 노출되는 영역이 다르므로 따로 따로 반환
        # return task_complete_process, inspect_complete_process, length_to_task, length_to_inspect


    ## 관리자 페이지의 검토 페이지 (승인, 반려)에 들어가는 데이터를 가져오는 로직
    def get_task_check_data(self, request):

        # orm
        # get_all_task = WorkList.objects.filter(task_status = 'C')

        # sql
        sqlMethodClass = sqlMethod()
        column_list = None
        try:
            # 작업이 완료되고 반려된 인스턴스들
            get_all_task = sqlMethodClass.select_workList(table_name="django_app_worklist", data_dic={'1':'1'}, status_list={dbinfo.status['status_1cha_inspect_deagi'], dbinfo.status['status_1cha_companion_return'], dbinfo.status['status_2cha_companion_return'], dbinfo.status['status_3cha_companion_return']}, column_list=column_list, option=" order by work_id desc")
            # print(get_all_task)
        except:
            raise

        task_name_list = []
        inspect_name_list = []
        record_key_list = []

        for item in get_all_task :
            # orm
            #print("worklist 기본 키 : ", item.task_num)
            #query_set = WorkRecord.objects.filter(worklist_task_num_id = item.task_num, work_category = 'T', work_state = "False")
            ## filter 대신 get으로 가져오게 될 경우 데이터가 존재하지 않을 경우를 대비해서 filter로 exists() 체크를 하는 것이 바람직

            print(item)
            # sql
            try:
                query_set = sqlMethodClass.select_workList(table_name="django_app_workhistory", data_dic ={"work_id":str(item.get("work_id"))}, status_list={"T"}, column_list=column_list)
            except:
                raise

            if len(query_set) > 0 :
                # orm
                #get_record_data = WorkRecord.objects.get(worklist_task_num_id = item.task_num, work_category = 'T', work_state = "False")
                #get_worklist_data = WorkList.objects.get(task_num = get_record_data.worklist_task_num_id)

                #get_user_name = Profile.objects.get(account_id = get_worklist_data.task_user_id)
                
                #record_key_list.append(get_record_data.worklist_task_num_id)
                #task_name_list.append(get_user_name.user_name)

                # sql
                try:
                    get_record_data = sqlMethodClass.select_workList(table_name="django_app_workhistory", data_dic ={"work_id":item.get("task_num")}, status_list={"T"}, column_list=column_list)
                    get_worklist_data = sqlMethodClass.select_workList(table_name="django_app_worklist", data_dic={"work_id":get_record_data.get("work_id")}, column_list=column_list)

                    get_user_name = sqlMethodClass.select_workList(table_name="django_app_profile", data_dic={"account_id":get_worklist_data.get("worker_id")}, column_list=column_list)
                except:
                    raise

                record_key_list.append(get_record_data.get("work_id"))
                task_name_list.append(get_user_name.get("user_name"))
            
        return zip(get_all_task, task_name_list, record_key_list)


    ## 관리자 페이지 내 작업의 승인을 처리하기 위한 로직
    def task_status_change(self, request, record_key, message) :

        ## 매개변수로 받은 message를 조건으로 작업이 승인인 경우와 반려인 경우를 처리

        ## 작업 승인인 경우
        if message == "approve" :

            try:
                task = WorkRecord.objects.get(worklist_task_num_id = record_key, work_category = "T")
                task_complete = WorkRecord.objects.get(worklist_task_num_id = record_key, work_category = "Q")
            except:
                raise

            task.work_approved_date = datetime.now()
            task.work_state = "True"

            task_complete.work_approved_date = datetime.now()
            task_complete.work_state = "True"

            task.save()
            task_complete.save()

            add_task = WorkRecord()

            add_task.task_num = task.task_num
            add_task.work_category = "Y"
            add_task.reg_id = task.reg_id
            add_task.reg_date = datetime.now()
            add_task.worklist_task_num_id = record_key
            add_task_approved_date = datetime.now()
            add_task.work_state = "True"

            add_task.save()
            

        ## 작업 반려인 경우 
        else :

            # task = WorkRecord.objects.get(worklist_task_num_id = record_key, work_category = "T")

            try:
                task_complete = WorkRecord.objects.get(worklist_task_num_id = record_key, work_category = "Q")
            except:
                raise
            task_complete.work_category = "N"

            task_complete.save()


            worklist = WorkList.objects.get(task_num = record_key)

            worklist.task_status = "B"

            worklist.save()

        
        return 200


    ## 관리자 페이지 내 작업 현황에 뿌려주는 데이터를 가져오는 로직
    def get_current_process(self, request, data_dic=None):
        print('get_current_processㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        if data_dic == None :
            option = ""
        else :
            print(data_dic)
            print(data_dic['workerNm'])
            print(data_dic['workType'])
            print(data_dic['workStatus'])
            print(data_dic['searchBgn'])
            print(data_dic['searchEnd'])
            option = ""
            if data_dic['workerNm'] != '':
                option = option + "and (worker_name1 = '"+data_dic['workerNm']+"'" +\
                        "or worker_name2 = '"+data_dic['workerNm']+"'" +\
                        "or worker_name3 = '"+data_dic['workerNm']+"'" +\
                        "or worker_name4 = '"+data_dic['workerNm']+"') limit 200"

            elif data_dic['workType'] != '':
                option = option + "and str_type = '"+data_dic['workType']+"'"

            elif data_dic['workStatus'] != '':
                option = option + "and work_status = '" + data_dic['workStatus']+"'"

            elif data_dic['searchBgn'] != '' and data_dic['searchEnd'] != '':
                option = option + "and reg_date BETWEEN TO_TIMESTAMP('"+data_dic['searchBgn']+"', 'YYYY-MM-DD') AND TO_TIMESTAMP('"+data_dic['searchEnd']+"', 'YYYY-MM-DD')  + interval '1 day'"

            elif data_dic['groupId'] != '' and data_dic['groupId'] != 'all':
                option = option + "and group_id = '" + data_dic['groupId']+"'"
            elif data_dic['groupId'] == 'all':
                option = option + "and group_id = 'tbit' or group_id = 'gjac' or group_id = 'dtw'"

        sqlMethodClsss = sqlMethod()
        dic = {}
        table = "(select  * , "+\
                "(select dap.user_name from django_app_profile dap where dap.account_id = daw.worker_id) worker_name1, "+\
                "(select dap.user_name from django_app_profile dap where dap.account_id = daw.inspect_id1) worker_name2, "+\
                "(select dap.user_name from django_app_profile dap where dap.account_id = daw.inspect_id2) worker_name3, "+\
                "(select dap.user_name from django_app_profile dap where dap.account_id = daw.inspect_id3) worker_name4, "+\
                "(select dacm.code_nm from django_app_code_mst dacm where dacm.code_id = daw.work_status ) str_status, "+\
                "(select dacm.code_nm from django_app_code_mst dacm where dacm.code_id = daw.work_type) str_type "+\
                "from django_app_worklist daw "+\
                "where 1 = 1 order by work_id ) a  "
        try:
            get_all_task = sqlMethodClsss.select_workList(table_name=table, data_dic=dic, option=option)
        except:
            raise

        task_name_list = []
        inspect_name_list = []

        # print("get_all_task", get_all_task)
        ## WorkRecord의 데이터뿐만 아니라 WorkList의 데이터도 필요하므로 List의 길이를 맞추어서 조합해서 처리
        # for item in get_all_task :
        #     print("item-------------------------------", item)
        #     #print("tasker : ", item.task_user_id)
        #     #print("inspector", item.inspect_user_id)

        #     # query_2 = Profile.objects.filter(account_id = item.task_user_id)
        #     # query_2 = sqlMethodClsss.select_workList(table_name="django_app_profile", data_dic ={"account_id": item.get("worker_id")})
            
        #     try:
        #         user_name = sqlMethodClsss.select_workList(table_name="django_app_profile", data_dic ={"account_id": item.get("worker_id")}, column_list={"user_name"})
        #         tasker_name = user_name

        #         print("user***************", tasker_name)

        #         inspector = sqlMethodClsss.select_workList(table_name="django_app_profile", data_dic ={"account_id": item.get("inspect_id1")}, column_list={"user_name"})
        #         inspector_name = inspector


        #         print("inspector_name***************", inspector_name)

                

            
        #         task_name_list.append(tasker_name)
        #         inspect_name_list.append(inspector_name)

        #     # if len(query_2)>0 :
            
        #     #     # tasker = Profile.objects.get(account_id = item.task_user_id)
        #     #     user_name = sqlMethodClsss.select_workList(table_name="django_app_profile", data_dic ={"account_id": item.get("worker_id")}, column_list={"user_name"})
        #     #     tasker_name = user_name

        #         # return zip(get_all_task, task_name_list, inspect_name_list)

        #     # else:
        #     except:

        #         tasker_name = "NULL"
        #         inspector_name = "NULL"

            
        #         task_name_list.append(tasker_name)
        #         inspect_name_list.append(inspector_name)




        sqlMethodClsss.close()
        return get_all_task

            # query = Profile.objects.filter(account_id = item.inspect_user_id)

            # if query.exists():
                
            #     inspector = Profile.objects.get(account_id = item.inspect_user_id)
            #     inspector_name = inspector.user_name
            
            # else : 







    
    ## 관리자 페이지에서 유저의 권한을 변경 시 사용되는 로직
    def user_info_change(self, request):
        
        try : 

            user_name = request.POST.get("user_name","")
            print(user_name)
            staff = str("workAuth" in request.POST)
            inspector = str("inspectAuth" in request.POST)

            account_id = request.POST.get('user_account_id',"")

            user_model = User.objects.get(username = account_id)
            profile_model = Profile.objects.get(account_id = account_id)


            user_model.is_staff = staff
            profile_model.is_staff = staff
            profile_model.is_inspector = inspector

            user_model.save()
            profile_model.save()


            return True

        except :

            return False


    ## 관리자 페이지에서 상품 이름 선택 시 해당 상품을 가져오는 로직(ajax)
    # def get_detail_info(self, request, task_num):

    #     sql_query = sqlMethod()
    #     # info = WorkList.objects.get(task_num = task_num)
    #     info_dic = {"work_id" : task_num}
    #     info = sql_query.select_workList(table_name="django_app_worklist", data_dic=info_dic)

    #     # tasker_id = info.task_user_id
    #     # inspector_id = info.inspect_user_id
    #     tasker_id = info.get("worker_id")
    #     inspector_id1 = info.get("inspect_id1")
    #     inspector_id2 = info.get("inspect_id2")
    #     inspector_id3 = info.get("inspect_id3")

    #     tasker = Profile.objects.get(account_id = tasker_id)
    #     inspector1 = Profile.objects.get(account_id = inspector_id1)
    #     inspector2 = Profile.objects.get(account_id = inspector_id2)
    #     inspector3 = Profile.objects.get(account_id = inspector_id3)

    #     task_filter = WorkRecord.objects.filter(worklist_task_num_id = unique_key, work_category = 'T')

    #     ## 작업이 존재하는 경우
    #     if task_filter.exists():


    #         task_info = WorkRecord.objects.get(worklist_task_num_id = unique_key, work_category = 'T')
    #         task_unique_key = task_info.id
    #         task_process = len(TaskHistory.objects.filter(work_num_id = task_unique_key))
    #         task_process = task_process/image_full_count * 100


    #     ## 작업이 존재하지 않는 경우
    #     else :

    #         tasker_id = "None"
    #         task_process = "None"
            

    #     inspect_filter = WorkRecord.objects.filter(worklist_task_num_id = unique_key, work_category = 'I')
        
    #     ## 검수가 존재하는 경우
    #     if inspect_filter.exists():

    #         inspect_info = WorkRecord.objects.get(worklist_task_num_id = unique_key, work_category = 'I')
    #         inspect_unique_key = inspect_info.id
    #         inspect_process = len(InspectHistory.objects.filter(work_num_id = inspect_unique_key))
    #         inspect_process = inspect_process/image_full_count * 100
            
    #     ## 검수가 존재하지 않는 경우
    #     else :

    #         inspector_id = "None"
    #         inspect_process = "None"


    #     return tasker_id, inspector_id, task_process, inspect_process

    
    ## 관리자 페이지 내에서 작업 내용 확인 시 사용되는 로직
    def task_rework_logic(self, request, task_num):
        #print("Task Rework Logic")

        query = WorkList.objects.filter(task_num = task_num)
        if query.exists():

            return True

        else :

            return False

        

    ## 관리자 페이지 내에서 검수 내용 확인 시 사용되는 로직
    def inspect_rework_logic(self, request, task_num):
        #print('Inspect Rework Logic')

        query = WorkList.objects.filter(task_num = task_num)

        if query.exists():

            return True

        else :

            return False

        

    ## 장고 템플릿 언어로 작업 확인 페이지에 뿌려지는 데이터를 가져오는 로직 (Exists, NotExists를 판별하기 위한 로직)
    def get_task_info(self, request, task_num):

        query_set = WorkList.objects.all()

        try:
            check_point = query_set.filter(task_status = 'C', task_num = task_num)
            check_point_2 = query_set.filter(task_status = 'B', task_num = task_num)
        except:
            raise

        if check_point.exists():

            ## 작업 완료된 작업을 부를 경우
            #print("작업이 완료된 경우")

            return check_point
        
        elif check_point_2.exists():

            ## 작업이 완료되지 않은 경우
            #print("작업이 완료되지 않은 경우")

            return check_point_2

        else :

            #print("검색된 작업이 존재하지 않음")

            return False
            

    ## 장고 템플릿 언어로 검수 확인 페이지에 뿌려지는 데이터를 가져오는 로직 (Exists, NotExists를 판별하기 위한 로직)
    def get_inspect_info(self, request, task_num):

        query_set = WorkList.objects.all()

        try:
            check_point = query_set.filter(inspect_status = 'C', task_num = task_num)
            check_point_2 = query_set.filter(inspect_status = 'B', task_num = task_num)
        except:
            raise

        if check_point.exists():

            ## 검수 완료된 작업을 부를 경우
            #print("검수가 완료된 경우 로직 구성")

            return check_point
        
        elif check_point_2.exists() :

            ## 검수가 완료되지 않은 경우
            #print("검수가 완료되지 않은 경우 로직 구성")

            return check_point_2
        
        else :

            #print("검색된 검수 작업이 존재하지 않음")

            return False




    ## 관리자 페이지 내 Task DB 정보 체크
    ## 작업 페이지에 Label등 정보를 다시 그리기 위해 DB에서 꺼내서 json 데이터를 재조합하는 로직
    def task_check_db_data(self, request, task_num):

        #print("Check Task DB Data")
        
        ## binary to string 기능
        def return_string(*argument):
                
            convert_data = bytes(*argument, 'utf8')
            convert_data = convert_data.decode('utf-8')

            return convert_data

        get_json_data = json.loads(request.body)

        ## ajax로 받아온 데이터를 체크
        #print("ajax Data : ", get_json_data)

        try:
            condition_check = WorkRecord.objects.filter(task_num = task_num, work_category = "Q")
        except:
            raise

        if condition_check.exists():

            try:
                get_record = WorkRecord.objects.get(work_category = "T", task_num = task_num, worklist_task_num_id = get_json_data)
            except:
                raise
            record_key_2 = get_record.id

            try:
                get_tasklist = TaskHistory.objects.filter(work_num_id = record_key_2).order_by('task_image_num')
            except:
                raise

            ## json 데이터를 재조합하는 과정
            get_id_list, get_width_list, get_height_list = [],[],[]
            get_scaleX_list, get_scaleY_list, get_name_list = [],[],[]
            get_images_list, get_path_list, get_type_list, get_length_list = [],[],[],[]


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

                data_path = return_string(task_data['path'])
                get_path_list.append(data_path)

                data_length = task_data['length']
                get_length_list.append(data_length)

                data_type = return_string(task_data['type'])
                get_type_list.append(data_type)
            

            #print("*********** || ReCombine Task Data || *************")
            
            recombine_dict = {"id": get_id_list[0],"width":get_width_list[0], "height":get_height_list[0], "scaleX":get_scaleX_list[0], "scaleY":get_scaleY_list[0], "name":get_name_list[0], "images":"["+"]", "length":get_length_list[0], "path":get_path_list[0], "type":get_type_list[0]}
            
            ## 조합 시 문제가 되는 부분이 존재해서 라벨 부분만 리스트로 따로 프론트로 보냄
            return recombine_dict, get_images_list
            
    
    ## 관리자 페이지 내 Task DB 정보 체크 
    ## 검수 페이지에 Label등 정보를 다시 그리기 위해 DB에서 꺼내서 json 데이터를 재조합하는 로직
    def inspect_check_db_data(self, request, task_num):

        #print("Check Inspect DB Data")

        def return_string(*argument):
                
            convert_data = bytes(*argument, 'utf8')
            convert_data = convert_data.decode('utf-8')

            return convert_data


        get_json_data = json.loads(request.body)

        #print("Get Json Data : ",get_json_data)

        try:
            condition_check = WorkRecord.objects.filter(task_num = task_num, work_category = "U")
        except:
            raise

        if condition_check.exists() :    

            user_name = request.user

            try:
                get_record = WorkRecord.objects.get(work_category = "I", task_num = task_num, worklist_task_num_id = get_json_data)
            except:
                raise
            record_unique_key = get_record.id

            try:
                get_tasklist = InspectHistory.objects.filter(work_num_id = record_unique_key).order_by('inspect_image_num')
            except:
                raise

            get_id_list, get_width_list, get_height_list = [],[],[]
            get_scaleX_list, get_scaleY_list, get_name_list = [],[],[]
            get_images_list, get_path_list, get_type_list, get_length_list = [],[],[],[]


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

                

                data_path = return_string(task_data['path'])
                get_path_list.append(data_path)

                data_length = task_data['length']
                get_length_list.append(data_length)

                data_type = return_string(task_data['type'])
                get_type_list.append(data_type)
            


            #print("*********** || ReCombine Inspect Data || *************")

            
            recombine_dict = {"id": get_id_list[0], "width":get_width_list[0], "height":get_height_list[0], "scaleX":get_scaleX_list[0], "scaleY":get_scaleY_list[0], "name":get_name_list[0], "images":"["+"]", "length":get_length_list[0], "path":get_path_list[0], "type":get_type_list[0]}

            ## 조합 시 문제가 되는 부분으로 라벨 부분은 리스트로 따로 프론트로 보냄
            return recombine_dict, get_images_list


        else:
            
            
            #print("검수가 완료되기 전 데이터입니다.")
            return False

