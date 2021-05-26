import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from nms_server.dao.redis import domain
from nms_server.utils import error_code

logger = logging.getLogger("nms." + __name__)

# service
class ServiceDomainTree(APIView):
    def get(self, request):
        parentMoid = request.data.get('parentMoid')

        logger.info('[ServiceDomainTree] parentMoid : %s' % parentMoid)

        if parentMoid == None:
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                # 服务域树，仅获取服务域节点，固传递服务域参数
                parentMoid = user['data']['serviceDomainMoid']
            else:
                response = {'success':0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        response = {'success': 1}
        response["data"] = domain.get_service_domain_tree(parentMoid)
        return Response(response)

# user
class UserDomainTree(APIView):
    def get(self, request):
        parentMoid = request.data.get('parentMoid')

        logger.info('[UserDomainTree] parentMoid : %s' % parentMoid)

        if parentMoid == None:
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success':0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        response = {'success': 1}
        response["data"] = domain.get_user_domain_tree(parentMoid)
        return Response(response)

# platform
class PlatformDomainTree(APIView):
    def get(self, request):
        parentMoid = request.data.get('parentMoid')
        
        logger.info('[PlatformDomainTree] parentMoid : %s' % parentMoid)

        if parentMoid == None:
            user = getattr(request, 'sso_user', None)
            if user is not None:
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success':0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)
                
        response = {'success': 1}
        response["data"] = domain.get_platform_domain_tree(parentMoid)
        return Response(response)


# 获取从顶级域开始的整个域树
class DomainTree(APIView):
    def get(self, request):
        logger.info('start get domain tree')

        response = {'success': 1}
        response["data"] = domain.get_domain_list('-1')
        return Response(response)

class MachineRoomMoid(APIView):
    def get(self, request):
        parentMoid = request.data.get('parentMoid')
        logger.info('[MachineRoomMoid] parentMoid : %s' % parentMoid)

        if parentMoid == None or parentMoid == '':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success':0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        response = {'success': 1}
        response["data"] = domain.get_machine_room_moid_list(parentMoid)
        return Response(response)

class UserDomainMoid(APIView):
    def get(self, request):
        parentMoid = request.data.get('parentMoid')
        logger.info('[UserDomainMoid] parentMoid : %s' % parentMoid)

        if parentMoid == None or parentMoid == '':
            user = getattr(request, 'sso_user', None)
            if user is not None: 
                parentMoid = user['data']['accountDomainMoid']
            else:
                response = {'success':0,"error_code":error_code.UN_LOGIN, 'message':'未登陆用户'}
                return Response(response)

        response = {'success': 1}
        response["data"] = domain.get_user_domain_moid_list(parentMoid)
        return Response(response)
        