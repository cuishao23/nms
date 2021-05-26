from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^loginfo$', LogInfoList.as_view()),
    url(r'^downloadlog$', DownloadLog.as_view())
]
