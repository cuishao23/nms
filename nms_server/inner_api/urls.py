from django.conf.urls import url
from . import views
from .views import *
from nms_server.nms_inspect import views as inspect_views
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # url(r'docs/', include_docs_urls(title="后台接口")),
    url(r'^terminal_type$', BmcTerminalType.as_view()),      # 终端型号，bmc使用

    url(r'^resource/(?P<domain_moid>[-\w]+)/media_vmr_statistic$', MediaResourceStatistic.as_view()),    #媒体资源
    url(r'^warning/topn_unrepaired$', UnrepairedWarning.as_view()),      #服务器n条最新未修复告警信息

    url(r'^meeting/(?P<domain_moid>[-\w]+)/meeting_statistic$', MeetingStatistic.as_view()),   # 并发会议统计数据
    url(r'^meeting/(?P<domain_moid>[-\w]+)/terminal_statistic$', TerminalStatistic.as_view()),  # 并发会议在线终端统计信息
    url(r'^terminal/(?P<domain_moid>[-\w]+)/online_statistic$', TerminalOnlineStatistic.as_view()),   # 在线终端统计信息

    url(r'^physicals$', Physicals.as_view()),       # 物理服务器列表
    url(r'^physicals/resource$', PhysicalsResource.as_view()),     # 服务器的硬件资源信息列表
    url(r'^physicals/topn/cpu$', PhysicalsByCpu.as_view()),      #CPU使用率前n的物理服务器
    url(r'^physicals/topn/memory$', PhysicalsByMemory.as_view()),   #内存使用率前n的物理服务器
    url(r'^physicals/(?P<p_server_moid>[-\w]+)/cpu_history$', PhysicalCpuHistory.as_view()),     # 获取物理服务器cpu历史
    url(r'^physicals/(?P<p_server_moid>[-\w]+)/memory_history$', PhysicalMemoryHistory.as_view()),  # 物理服务器内存历史
    url(r'^physicals/usb_storage_state$', physicalsUsbStorageState.as_view()),     # 物理服务器的u盘状态
    
    url(r'^domains$', Domains.as_view()),     # 域信息
    url(r'^domains/(?P<domain_moid>[-\w]+)/lives$', Lives.as_view()),   # 域所属直播列表
    url(r'^domains/(?P<domain_moid>[-\w]+)/appointment/list$', AppointmentMeetings.as_view()),    # 域所属预约会议列表
    url(r'^domains/(?P<domain_moid>[-\w]+)/appointment/history$', AppointmentMeetingStatistic.as_view()),     # 预约会议统计数据
    url(r'^domains/(?P<domain_moid>[-\w]+)/meetings$', Meetings.as_view()),    # 域所属实时会议列表
    url(r'^domains/(?P<domain_moid>[-\w]+)/meetings/history$', HistoryMeetings.as_view()),    #域所属历史会议列表
    url(r'^domains/(?P<domain_moid>[-\w]+)/aplives$', Aplives.as_view()),     #域所属预约直播列表

    url(r'^terminal/(?P<terminal_moid>[-\w]+)/(?P<terminal_type>[-\w]+)/diagnosis$', TerminalDiagnosis.as_view()),  # 终端诊断结果（暂不实现，可从rmq消息抓取）
    url(r'^terminal/(?P<param_type>[-\w]+)/(?P<param_value>[-\w\.]+)/detail$', TerminalDetail.as_view()),      # 终端丢包率详情    
    # starter用巡检api
    url(r'^inspect/(?P<taskid>\d+)/$', inspect_views.InspectView.as_view()),

]
