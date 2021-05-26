from django.conf.urls import url
from .views import *
from . import views

urlpatterns = [
    url(r'^versions/$', DevVerinfoList.as_view()),
    url(r'^versiondetails/(?P<name>[a-zA-Z0-9-\u4E00-\u9FA5\S\s]+)/$', DevVerinfoDetail.as_view()),
    url(r'^addverinfo/$', views.addverinfo, name='addverinfo'),
    url(r'^editver/$', views.editver, name='editver'),
    url(r'^deletever/$', views.deletever, name='deletever'),
    url(r'^uploadverfile/$', views.uploadverfile, name='uploadverfile'),
    url(r'^existver/$', views.existver, name='existver'),
    url(r'^download/([a-zA-Z]+)/([0-9a-zA-Z\S\s]+)/([0-9\S\s]+)/([a-zA-Z\S\s]+)/$', views.download, name='download'),
    url(r'^version/$', VerinfoList.as_view()),
]
