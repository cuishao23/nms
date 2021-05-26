import logging
import os
from rest_framework import generics
from nms_server.dao import sus
from nms_server.dao.mysql.sus import *
from django.http import FileResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .utils import get_file_md5
from rest_framework.views import APIView
from nms_server.utils import error_code
import shutil

logger = logging.getLogger('nms.'+__name__)

# 版本信息数据列表
class DevVerinfoList(APIView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('newPageNum')
        deviceType = request.GET.get('deviceType')

        if page == None or page == '':
            response = {'success':0,"error_code":error_code.INPUT_ERROR, 'message':'参数错误'}
            return Response(response)

        if deviceType == None or deviceType == '':
            deviceType = 'all'

        logger.info('[DevVerinfoList] page:%s' % page)
        logger.info('[DevVerinfoList] deviceType:%s' % deviceType)

        dev_list, total_num = sus.get_version_list(page, deviceType)
        logger.info('[DevVerinfoList] dev_list: %s,total_num: %s'%(dev_list, total_num))

        response = {'success': 1}
        response['data'] = dev_list
        response['total_num'] = total_num
        return Response(response)

# 单个版本信息数据
class DevVerinfoDetail(generics.RetrieveUpdateAPIView):
    serializer_class = sus.DevVerinfoSerializer
    queryset = DevVerInfo.objects.all()
    lookup_field = 'name'

    def get_queryset(self):
        return DevVerInfo.objects.filter(device_type=self.kwargs['name'])

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = sus.DevVerinfoSerializer(queryset, many=True)
        return Response({ 'data': serializer.data})

# 上传的版本信息保存到mysql数据库
def addverinfo(request): 
    if request.method == 'GET':
        return JsonResponse({"success":0,"error_code":error_code.METHOD_ERROR})
    elif request.method == 'POST':
        oem_mark = request.POST.get('oem_mark')
        device_type = request.POST.get('device_type')
        device_type_file = ('_').join(device_type.split(" "))
        ver_level = request.POST.get('ver_level')
        release_attribute = request.POST.get('release_attribute')
        soft_ver = request.POST.get('soft_ver')
        release_notes = request.POST.get('release_notes')
        file_name = request.POST.get('file_name')
        file_size = request.POST.get('file_size')
        grayrange_moidlist = request.POST.get('grayrange_moidlist')
        grayrange_e164list = request.POST.get('grayrange_e164list')

        softVer = soft_ver.replace("V","")
        softVer = softVer.replace("v","")
        # 计算md5
        md5 = get_file_md5("/mnt/files/susmgr/version/" + oem_mark + "/" + device_type_file + "/" + softVer + "/%s" % file_name)
        
        try:
            result = sus.save_version_info(oem_mark, device_type, ver_level, release_attribute, soft_ver, release_notes, file_name, file_size, grayrange_moidlist, grayrange_e164list, md5)
            if result:
                return JsonResponse({"success": 1})
            else:
                return JsonResponse({"success": 0,"message":"存在相同版本属性"})
        except Exception as e:
            logger.error(e)
            return JsonResponse({"success": 0,"message":"版本信息保存失败"})


# 接收上传的版本文件
@csrf_exempt
def uploadverfile(request):
    # 请求方法为POST时，进行处理
    if request.method == "POST":
        # 获取上传的文件，如果没有文件，则默认为None
        File = request.FILES.get("file", None)
        device_type = request.POST.get("device_type")
        device_type = device_type.replace(" ", "_")
        soft_ver = request.POST.get("soft_ver")
        oem_mark = request.POST.get("oem_mark")

        soft_ver = soft_ver.replace("V","")
        soft_ver = soft_ver.replace("v","")

        if File is None:
            return JsonResponse({'success':0,'message':'文件信息为空'})
        else:
            filepath='/mnt/files/susmgr/version/'+oem_mark+'/'+device_type+'/'+soft_ver
            logger.info("[uploadfiles] file path : %s" % filepath)

            # 残留老的版本文件，则删除
            if os.path.exists(filepath):
                shutil.rmtree(filepath,ignore_errors=True) 

            os.makedirs(filepath)
            with open("/mnt/files/susmgr/version/"+oem_mark+"/"+device_type+"/"+soft_ver+"/%s" % File.name, 'wb+') as f:
                # 分块写入文件
                for chunk in  File.chunks():
                    f.write(chunk)
            f.close()
            return JsonResponse({"success": 1})
    else:
        return JsonResponse({"success":1, "error_code":error_code.METHOD_ERROR})

# 编辑版本信息
def editver(request):
    ver_sn = request.POST.get('ver_sn')
    ver_level = request.POST.get('ver_level')
    release_attribute = request.POST.get('release_attribute')
    release_notes = request.POST.get('release_notes')
    grayrange_moidlist = request.POST.get('grayrange_moidlist')
    grayrange_e164list = request.POST.get('grayrange_e164list')
    tip = request.POST.get('tip')

    result = sus.edit_verinfo(ver_sn, ver_level, release_attribute, release_notes, grayrange_moidlist, grayrange_e164list, tip)

    if result == 1:
        return JsonResponse({"success": 1})
    elif result == 2:
        return JsonResponse({"success": 2,"message":"存在相同版本属性"})
    else:
        return JsonResponse({"success": 0,"message":"数据库错误"})

# 删除版本信息
def deletever(request):
    ver_sn = request.POST.get('ver_sn')

    # 先删除数据库信息，再删除文件，文件如果删除失败，影响不大
    oem_mark, device_type, soft_ver = sus.delete_version(ver_sn)
    device_type = device_type.replace(" ", "_")
    soft_ver = soft_ver.replace("V","")
    soft_ver = soft_ver.replace("v","")

    dirpath = "/mnt/files/susmgr/version/"+oem_mark+'/'+device_type+"/"+soft_ver
    logger.info('delete file path : %s'%dirpath)

    # 删除文件和文件夹
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath,ignore_errors=True) # 删除文件及所在的文件夹
    else:
        logger.info('no such file:%s' % dirpath)
        return JsonResponse({"success": 0})

    return JsonResponse({"success": 1})

# 查询同一oem同一终端类型是否已经存在同一版本类型
def existver(request):
    device_type = request.POST.get('device_type')
    oem_mark = request.POST.get('oem_mark')
    soft_ver = request.POST.get('soft_ver')

    result = sus.exist_verinfo(device_type, oem_mark, soft_ver)
    
    if result == 1:
        return JsonResponse({"success": 1})
    else:
        return JsonResponse({"success": 0})


# SUS下载版本文件接口
def download(request,oem,devicetype,softver,filename):

    logger.info('file down info : oem=%s, devicetype=%s, softver=%s, filename=%s'%(oem,devicetype,softver,filename))
    
    # 去掉设备类型里面的空格
    devicetype = devicetype.replace(" ", "_")

    # 去掉版本号里面的V和v
    softver = softver.replace("V","")
    softver = softver.replace("v","")
    
    try:
        file = open('/mnt/files/susmgr/version/' + oem + '/' + devicetype + '/' + softver + '/' + filename, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % (filename)
    except:
        return JsonResponse({'success': 0}, status=404)
    else:
        return response

# SUS获取版本信息列表的接口
class VerinfoList(APIView):
    def get(self, request, *args, **kwargs):
        try:
            oemmark = request.GET.get('oemmark')
            oemmark_list = oemmark.split(',')
            ver_list = [2, 4]
            ver_info_list = sus.filter_ver_info_list(oemmark_list, ver_list)
            response = {'success': 1}
            response['data'] = ver_info_list
        except Exception as e:
            logging.warning('get sus version info list failed')
            logger.info('[VerinfoList] reason:%s'%e)
            return JsonResponse({'success': 0,'error_code':'404'})
        else:
            return Response(response)
