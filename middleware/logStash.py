import logging
from django.urls.resolvers import get_resolver
from .log_operator_content_dict import VerifyUrlSaveContent
from rest_framework.response import Response
from django.http import FileResponse
from nms_server.dao.opr_log import operate_log

logger = logging.getLogger("nms." + __name__)

CONST_METHODS = dict(GET="查看", POST="新增", PUT="修改", DELETE="删除")

URL_REGEX = get_resolver()

def logStashMiddleware(get_response):
    def middleware(request):
        response = get_response(request)
        if request.path.startswith('/nms/check'):
            return response
        try:
            verify_url_save_content = VerifyUrlSaveContent(request, response)
            detail = verify_url_save_content.run()
            if detail is not None:
                operate_log(detail)
        except Exception as e:
            logger.error(e)
            pass
        return response
    return middleware

