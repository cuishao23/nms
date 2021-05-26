from django.shortcuts import render
from django.conf import settings
from django.middleware.csrf import rotate_token
from rest_framework.views import APIView
from rest_framework.views import Response
from nms_server.utils.sso import user_log_out
# Create your views here.


class CheckView(APIView):
    def get(self, request, *args, **kwargs):
        return Response("nms is running normal")


class ServerInfoView(APIView):
    def get(self, request):
        user_info = getattr(request, 'sso_user', None)
        user = user_info['data']['account'] if user_info is not None else ''
        rotate_token(request)
        return Response({
            'user': user,
            'brand': settings.BRAND,
            'version': settings.VERSION,
            'user_domain': user_info['data']['userDomainAdmin'] or user_info['data']['defaultUserDomainAdmin'],
            'admin': (user_info['data']['serviceDomainAdmin'] or user_info['data']['defaultServiceDomainAdmin']) and user_info['data']['nmAdmin']
        })


class LogOutView(APIView):
    def post(self, request):
        user_info = getattr(request, 'sso_user', None)
        if user_info is None:
            return Response({'success': 1})
        else:
            user_log_out(user_info['data']['account'], request.COOKIES.get('SSO_COOKIE_KEY', ''))
            r = Response({'success': 1})
            r.delete_cookie('SSO_COOKIE_KEY')
            return r
