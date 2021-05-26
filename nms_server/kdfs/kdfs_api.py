from nms_server.httpool import get_http_session
from django.conf import settings
import logging

# kdfs url
KDFS_URL = '/api/inner/kdfs/v1'

# 每次读取长度
MAX_READ_LEN = 1024 * 64

# 下载文件时的头部
headers = {
    'type': 'download',
    'home': 'platformLog'
}

def __get_kdfs_config():
    '''
    获取kdfs地址
    :return:
    '''
    try:
        host = settings.KDFS.get('HOST')
        port = settings.KDFS.get('PORT')
        return host, port
    except Exception as e:
        logging.error('kdfs config error')
        raise e

def download_from_kdfs(filename, callback):
    '''
    从kdfs下载并处理文件内容
    :param filename: 文件名
    :param callback: callback(chunk), chunk为每次读取的内容
    :return:
    '''
    if not callback:
        logging.error('callback not set')
        return False
    host, port = __get_kdfs_config()
    url = 'httpool://' + host + ':' + str(port) + KDFS_URL
    session = get_http_session()
    headers['path'] = filename
    resp = session.get(url=url, headers=headers)
    resp.raise_for_status()
    # 循环读取文件内容
    for chunk in resp.iter_content(MAX_READ_LEN):
        callback(chunk)
