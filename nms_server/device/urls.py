from django.conf.urls import url
from nms_server.device import views

urlpatterns = [
    url(r'^servertypelist$', views.ServerTypeList.as_view()),
    url(r'^physicaltypelist$', views.PhysicalTypeList.as_view()),
    url(r'^frametypelist$', views.FrameTypeList.as_view()),
    url(r'^noframetypelist$', views.NoframeTypeList.as_view()),
    url(r'^frameinfo$', views.PhysicalFrameInfoList.as_view()),
    url(r'^physicaldetailinfo$', views.PhysicalServerDetailInfo.as_view()),
    url(r'^diskinfo$', views.PhysicalDiskInfo.as_view()),
    url(r'^terminaltypelist$', views.TerminalTypeList.as_view()),
    url(r'^terminals$', views.TerminalInfoList.as_view()),
    url(r'^terminalinfodownload$', views.TerminalInfoDownLoad.as_view()),
    url(r'^terminaldetail$', views.TerminalDetailInfo.as_view()),
    url(r'^terminalperipherals$', views.TerminalPeripherals.as_view()),
    url(r'^uncontroledterminal$', views.UncontroledTerminalList.as_view()),
    url(r'^rebootserver$', views.RebootServer.as_view()),
    url(r'^shutdownserver$', views.ShutdownServer.as_view()),
    url(r'^rebootterminal$', views.RebootTerminal.as_view()),
    url(r'^configterminalregaddr$', views.ConfigTerminalRegAddr.as_view()),
    url(r'^configterminalnetwork$', views.ConfigTerminalNetwork.as_view()),
    url(r'^configterminalvideoformat$', views.ConfigTerminalVideoFormat.as_view()),
    url(r'^onlineserver$', views.OnlineServerList.as_view()),
    url(r'^onlineterminal$', views.OnlineTerminalList.as_view()),
    url(r'^logicals$', views.LogicalServerList.as_view()),
    url(r'^terminalperformance$', views.TerminalPerformanceInfo.as_view()),
    url(r'^devicenamedetail$', views.DeviceNameDetail.as_view()),
    url(r'^serverinfo$', views.PhysicalServerInfoList.as_view())
]
