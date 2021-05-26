from django.conf.urls import url
from nms_server.nms_inspect import views

urlpatterns = [
    url(r'^$', views.InspectListView.as_view()),
    url(r'^(?P<taskid>\d+)/$', views.InspectView.as_view()),
    url(r'^download/$', views.DownloadView.as_view()),
    url(r'^(?P<taskid>\d+)/license/$', views.LicenseView.as_view()),
    url(r'^(?P<taskid>\d+)/resource/$', views.ResourceView.as_view()),
    url(r'^(?P<taskid>\d+)/server/$', views.ServerView.as_view()),
    url(r'^(?P<taskid>\d+)/terminal/$', views.TerminalView.as_view()),
    url(r'^(?P<taskid>\d+)/server/(?P<device_moid>[-\w]+)/resource/$', views.ServerResourceView.as_view()),
    url(r'^(?P<taskid>\d+)/(?P<device_type>(server|terminal))/(?P<device_moid>[-\w]+)/unrepairwarning/$', views.UnrepairWarningView.as_view()),
    url(r'^delete/$', views.DeleteInspectChildView.as_view()),
]
