import logging
import requests
from django.conf import settings


ACCOUNT_TOKEN_URL = 'http://{ip}:{port}/apiCore/accountToken'
ADMIN_AUTHENTICATE_URL = 'http://{ip}:{port}/apiCore/sso/checkAdministratorPassword'
USER_LOG_OUT_URL = 'http://{ip}:{port}/apiCore/sso/userLogout'
OAUTH_CONSUMER_KEY = "Nms"
OAUTH_CONSUMER_SECRET = "12345678"

logger = logging.getLogger("nms." + __name__)


def get_account_token(ip, port):
    import xml.etree.ElementTree as ET
    try:
        params = {
            'oauth_consumer_key': OAUTH_CONSUMER_KEY,
            'oauth_consumer_secret': OAUTH_CONSUMER_SECRET
        }
        url = ACCOUNT_TOKEN_URL.format(ip=ip, port=port)
        r = requests.post(url, params=params, timeout=settings.REQUESTS_TIMEOUT)
        root = ET.fromstring(r.text)
        token = root.findtext('accountToken')
        # logger.info('get account token success, token : %s' % token)
        return token
    except Exception as e:
        logger.error('get account token error! %s' % e)
        return ''


def admin_authenticate(password):
    account_token = get_account_token(settings.SSO_HOST, settings.SSO_PORT)
    try:
        data = {
            'account_token': account_token,
            'administratorPassword': password
        }
        url = ADMIN_AUTHENTICATE_URL.format(ip=settings.SSO_HOST, port=settings.SSO_PORT)
        r = requests.post(url, data=data, timeout=settings.REQUESTS_TIMEOUT)
        json_data = r.json()
        if json_data['success']:
            return True
    except Exception as e:
        logger.error(e)
    return False


def user_log_out(username, sso_token):
    account_token = get_account_token(settings.SSO_HOST, settings.SSO_PORT)
    url = USER_LOG_OUT_URL.format(ip=settings.SSO_HOST, port=settings.SSO_PORT)
    try:
        requests.post(url, params={
            'account_token': account_token,
            'userName': username,
            'ssoToken': sso_token
        }, timeout=settings.REQUESTS_TIMEOUT)
    except Exception as e:
        logger.error(e)