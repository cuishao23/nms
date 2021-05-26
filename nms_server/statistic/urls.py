from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^cpuchart/$', CpuChart.as_view()),
    url(r'^memchart/$', MemChart.as_view()),
    url(r'^netcardchart/$', NetcardChart.as_view()),
    url(r'^meetingquality/$', MetingQuality.as_view()),
    url(r'^meetingresource/$', MeetingResource.as_view()),
    url(r'^appointmeeting/$', AppointMeeting.as_view()),
    url(r'^cpuusage/$', CpuUsage.as_view()),
    url(r'^memusage/$', MemUsage.as_view()),
    url(r'^netcardup/$', NetcardUp.as_view()),
    url(r'^netcarddown/$', NetCardDown.as_view()),
    url(r'^warningstatistic/$', WarningStatistic.as_view()),
    url(r'^meetingstatistic/$', MeetingStatistic.as_view()),
    url(r'^serverstatistic/$', ServerStatistic.as_view()),
    url(r'^terminalstatistic/$', TerminalStatistic.as_view()),
    url(r'^diskagestatistic/$', DiskAgeStatistic.as_view()),
    url(r'^diskusagestatistic/$', DiskUsageStatistic.as_view()),
]