import logging
from rest_framework.response import Response

logger = logging.getLogger('nms.'+__name__)


def exception_handler(exc, context):
    if isinstance(exc, NotLoginError):
        logger.warning('not login error!')
    logger.error('exception_handler: view=%s, exception=%s' %
                 (context.get('view'), exc))
    return Response({'success': 0})


class NotLoginError(Exception):
    pass
