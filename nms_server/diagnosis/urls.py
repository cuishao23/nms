from django.conf.urls import url
from nms_server.diagnosis import views

urlpatterns = [
    url(r'^capturedevice/$', views.CaptureDevice.as_view()),
    url(r'^addcapturedevice/$', views.AddCaptureDevice.as_view()),
    url(r'^delcapturedevice/$', views.DeleteCaptureDevice.as_view()),
    url(r'^startcapturedevice/$', views.StartCaptureDevice.as_view()),
    url(r'^stopcapturedevice/$', views.StopCaptureDevice.as_view()),
    url(r'^capturefile/$', views.CaptureFile.as_view()),
    url(r'^downloadcapturefile/$', views.DownloadCaptureFile.as_view()),
    url(r'^capturelog/$', views.GetLogList.as_view()),
    url(r'^downloadcapturelog/$', views.DownloadLogFile.as_view()),
    url(r'^serverdiagnose/$', views.ServerDiagnose.as_view()),
    url(r'^terminaldiagnose/$', views.TerminalDiagnose.as_view())
]
