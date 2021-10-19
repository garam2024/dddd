from django.contrib import admin
from django.urls import path
# from django_app import views
from django.conf.urls.static import static
from django.conf import settings
# from django.views.static import serve 

from .views import admin_views, admin_return_views
from .views import base_views, task_views, task_views_abnormal, inspect_views_1st, inspect_views_2nd, inspect_views_3rd, \
    api_views, mypage_views

urlpatterns = [

    ## 관리자 메인 페이지
    path('index/', admin_views.adminIndex.as_view(), name='admin_index'),
    path('index/change_auth', admin_views.changeAuth, name='change_auth'), #(작업권한, 검수권한) 바꾸기
    path('index/get_search_data', admin_views.getSearchData, name='get_search_data'), #아작스 서치
    path('index/adminview', admin_return_views.adminTaskCheck.as_view(), name='adminview'),


    path('index/adminview/admin_complete', admin_return_views.admin_complete, name='admin_complete'),
    path('index/adminview/task_api', admin_return_views.task_api, name='task_api'),
    path("index/adminview/check_task", admin_return_views.check_task, name='check_task'),




    ## 진행 현황 데이터 Update Module(ajax)
    # path('index/product_data', admin_views.admin_update_module, name = 'update'),

    # 관리자 페이지 내 작업 확인용 페이지
    # path('adminTaskCheck/<str:product_name>/', admin_views.adminTaskCheck.as_view(), name = 'adminTaskCheck'),
    ## 관리자 페이지 내 검수 확인용 페이지
    # path('adminInspectCheck/<str:product_name>/', admin_views.adminInspectCheck.as_view(), name = 'adminInspectCheck'),

    ## 작업 내용 확인 시 DB를 참고하여 작업 페이지 재구성용 모듈(ajax)
    # path("adminTaskCheck/<str:product_name>/task_check_api", admin_views.task_check_api, name = 'task_check_api'),
    ## 검수 내용 확인 시 DB를 참고하여 검수 페이지 재구성용 모듈(ajax)
    # path("adminInspectCheck/<str:product_name>/inspect_check_api", admin_views.inspect_check_api, name = 'inspect_check_api'),

    # # 작업 승인용 모듈
    # path("adminTaskApprove/<str:record_key>", admin_views.admin_task_approve_module, name = 'admin_task_approve'),

    # ## 작업 반려용 모듈
    # path('adminTaskCancel/<str:record_key>', admin_views.admin_task_cancel_module, name = 'admin_task_cancel'),

    # ## 작업 반려 메시지 전송 모듈
    # path('refusemessage/<str:record_key>', views.get_refuse_message, name = 'refuse_message'),

    # 상민
    # 작업 등록
    path('index/insert_work', admin_views.insert_work, name='insert_work'),

]
