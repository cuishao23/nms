import logging
import json
import requests
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth
from nms_server.utils.sso import get_account_token

logger = logging.getLogger('nms.'+__name__)


# 过滤路由
AUTHENTICATE_FILTER = ('/api/inner/nms/', '/nms/check',
                       '/nms/home', '/nms/sus/download/', '/nms/sus/version/','/api/nms/version')

def authenticateMiddleware(get_response):
    def middleware(request):
        if settings.DEBUG and settings.DEBUG_COOKIE == "":
            # DEBUG模式, 未设置DEBUG_COOKIE时不验证
            request.csrf_processing_done = True
        elif not request.path.startswith(AUTHENTICATE_FILTER):
            if settings.DEBUG:
                request.csrf_processing_done = True
            if not is_authenticated(request):
                return JsonResponse({'success': 0}, status=401)
            else:
                try:
                    json_data = getattr(request, 'sso_user')           
                    if not json_data['data']['enableNM']:
                        return JsonResponse({'success': 0}, status=401)
                except Exception as e:
                    logger.error(e)
                    return JsonResponse({'success': 0}, status=401)

        # 在每一个响应前执行
        response = get_response(request)
        # 在每一个响应后执行
        return response
    return middleware


def is_authenticated(request):
    # 调试模式, 尝试后端验证
    if settings.DEBUG:
        sso_token = settings.DEBUG_COOKIE
    else:
        sso_token = request.COOKIES.get('SSO_COOKIE_KEY', '')
    account_token = get_account_token(settings.SSO_HOST, settings.SSO_PORT)
    if account_token:
        url = 'http://{ip}:{port}/apiCore/sso/validationToken'.format(
            ip=settings.SSO_HOST,
            port=settings.SSO_PORT)
        try:
            r = requests.post(
                url, data={'account_token': account_token, 'ssoToken': sso_token}, timeout=settings.REQUESTS_TIMEOUT)
            json_data = r.json()
            if json_data.get('success'):
                # sso 验证成功
                request.sso_user = json_data
                # 增加accountDomainMoid字段，保存账户所属域的moid，服务域账户即服务域moid，用户域账户，即用户域moid
                if ((json_data['data']['userDomainAdmin']) or (json_data['data']['defaultUserDomainAdmin'])):
                    request.sso_user['data']['accountDomainMoid'] = json_data['data']['userDomainMoid']
                else:
                    request.sso_user['data']['accountDomainMoid'] = json_data['data']['serviceDomainMoid']

                return True
        except Exception as e:
            logger.error(e)
    return False
