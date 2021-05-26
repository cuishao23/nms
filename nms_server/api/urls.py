from django.conf.urls import url
from . import views
from .views import *
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^version$', Version.as_view()),     # 版本信息
    url(r'^domains$', Domains.as_view()),     # 域信息
    url(r'^platform_domains/(?P<domain_moid>[-\w]+)/physicals$', Physicals.as_view()),   # 物理服务器列表
    url(r'^platform_domains/(?P<domain_moid>[-\w]+)/logicals$', Logicals.as_view()),   # 逻辑服务器及列表
    url(r'^user_domains/(?P<domain_moid>[-\w]+)/terminals$', Terminals.as_view()),   # 终端列表
    url(r'^physicals/(?P<p_server_moid>[-\w]+)/logicals$', LogicalsByPhysical.as_view()),   # 指定物理服务器下的逻辑服务器列表
    url(r'^physicals/(?P<p_server_moid>[-\w]+)/detail$', PhysicalDetail.as_view()),   # 指定物理服务器下的逻辑服务器列表    
    
    url(r'^old_terminals$', OldTerminals.as_view()),   # 非受管终端列表
    url(r'^old_terminals/(?P<terminal_ip>[-\w.]+)/detail$', OldTerminalDetail.as_view()),   # 非受管终端详情

    # 统计信息
    url(r'^service_domains/(?P<domain_moid>[-\w]+)/terminal_online_statistic$', TerminalOnlineStatistic.as_view()),   # 终端在线统计数据
    url(r'^user_domains/(?P<domain_moid>[-\w]+)/meetings$', Meetings.as_view()),   # 指定用户域下的实时会议列表
    url(r'^service_domains/(?P<domain_moid>[-\w]+)/meetings$', Meetings.as_view()),   # 指定服务域下的实时会议列表
    url(r'^meetings/(?P<conf_e164>[-\w]+)/terminal_detail$', MeetingTerminalDetail.as_view()),   # 指定服务域下的实时会议列表

    url(r'^platform_domains/(?P<domain_moid>[-\w]+)/mediaresources$', DomainMediaResource.as_view()),   # 媒体服务器列表
    url(r'^mediaresources/(?P<l_server_moid>[-\w]+)/portinfo$', ServerMediaResource.as_view()),   # 指定媒体服务器的资源

    url(r'^servers/(?P<server_moid>[-\w]+)/unrepaired_warnings$', ServerWarningUnrepaired.as_view()),   # 指定服务器的未修复告警
    url(r'^terminals/(?P<terminal_moid>[-\w]+)/unrepaired_warnings$', TerminalWarningUnrepaired.as_view()),   # 指定终端的未修复告警
]
