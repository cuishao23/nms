from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url="/nms/index.html")),
    url(r'^nms/home/$', RedirectView.as_view(url="/nms/index.html")),
    url(r'nms/check', views.CheckView.as_view()),
    url(r'nms/server_info/$', views.ServerInfoView.as_view()),
    url(r'nms/logout/$', views.LogOutView.as_view()),
]
