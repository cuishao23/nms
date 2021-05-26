from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^subserverwarning/$', ServerWarningSubList.as_view()),
    url(r'^subterminalwarning/$', TerminalWarningSubList.as_view()),
    url(r'^latestserverunrepairedwarning/$', ServerWarningUnrepairedList.as_view()),
    url(r'^latestterminalunrepairedwarning/$', TerminalWarningUnrepairedList.as_view()),
    url(r'^latestserverrepairedwarning/$', ServerWarningRepairedList.as_view()),
    url(r'^latestterminalrepairedwarning/$', TerminalWarningRepairedList.as_view()),
    url(r'^terminaldetailwarning$', TerminalDetailWarning.as_view()),
    url(r'^uncontroledterminalwarning/$', unControledTerminalWarningList.as_view()),
    url(r'^serverunrepairedwarning/$', ServerWarningUnrepaired.as_view()),
    url(r'^terminalunrepairedwarning/$', TerminalWarningUnrepaired.as_view()),
    url(r'^repairserverwarning/$', RepairServerWarning.as_view()),
    url(r'^repairterminalwarning/$', RepairTerminalWarning.as_view()),
    url(r'^downloadwarning/$', DownloadWarning.as_view())
]

