from django.conf.urls import url
from . import views
from .views import *


urlpatterns = [
    url(r'^resourcelimit/$', ResourceLimit.as_view()),
    url(r'^serverslimit/$', ServerLimit.as_view()),
    url(r'^deviceconfig/$', DeviceConfig.as_view()),
    url(r'^deldeviceconfig/$', DeleteDeviceConfig.as_view()),
    url(r'^terminaltypes/$', TerminalTypeList.as_view()),
    url(r'^warningtree/$', WarningTreeList.as_view()),
    url(r'^warningnotify/$', WarningNotify.as_view()),
    url(r'^delwarningnotify/$', DeleteWarningNotify.as_view()),
    url(r'^editwarningnotify/$', EditWarningNotify.as_view()),
    url(r'^subwarningcode/$', SubWarningCode.as_view()),
    url(r'^warninglevel/$', WarningLevel.as_view()),
    url(r'^stopwarning/$', StopWarning.as_view()),
    url(r'^devicetypelimit/$', DeviceTypeLimit.as_view()),
    url(r'^adddevicetypelimit/$', AddDeviceTypeLimit.as_view()),
    url(r'^deldevicetypelimit/$', DelDeviceTypeLimit.as_view()),
    url(r'^devicetypelimitcfg/$', DeviceTypeLimitCfg.as_view()),
]
