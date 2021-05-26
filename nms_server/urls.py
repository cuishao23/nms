# from django.contrib import admin
# from django.urls import path

import os
import logging
from django.conf.urls import url, include
from django.conf import settings
from django.views.generic.base import RedirectView

logger = logging.getLogger('nms.'+__name__)


urlpatterns = [
    url(r'^', include("misc.urls")),

    url('^nms/device/', include("device.urls")),            # to device
    url('^nms/diagnosis/', include("diagnosis.urls")),      # to diagnosis
    url('^nms/domain/', include("domain.urls")),            # to domain
    url('^nms/meeting/', include("meeting.urls")),          # to meeting
    url('^nms/opr_log/', include("opr_log.urls")),          # to opr_log
    url('^nms/sus/', include("sus.urls")),                  # to sus
    url('^nms/system_set/', include("system_set.urls")),    # to system_set
    url('^nms/warning/', include("warning.urls")),          # to warning
    url('^nms/inspect/', include("nms_inspect.urls")),      # to inspect
    url('^nms/ws/', include("ws.urls")),      				# to ws/websocket
    url('^nms/statistic/', include("statistic.urls")),      # to statistic

    # /api/v1/nms/
    url('^api/v1/nms/', include("api.urls")),               # to api
    url('^api/nms/', include("api.urls")),                  # to api version,无需认证
    # /api/inner/nms/
    url('^api/inner/nms/', include("inner_api.urls")),      # to inner api
]
