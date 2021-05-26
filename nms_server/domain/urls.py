from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^servicedomaintree/$', ServiceDomainTree.as_view()),
    url(r'^userdomaintree/$', UserDomainTree.as_view()),
    url(r'^platformdomaintree/$', PlatformDomainTree.as_view()),
    url(r'^domaintree/$', DomainTree.as_view()),
    url(r'^machineroommoid/$', MachineRoomMoid.as_view()),
    url(r'^userdomainmoid/$', UserDomainMoid.as_view()),
]
