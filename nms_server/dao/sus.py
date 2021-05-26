import logging
from nms_server.dao.mysql.sus import DevVerInfo
from rest_framework import serializers

logger = logging.getLogger('nms.'+__name__)

def getPage(page):
    if not page:
        page = 1
    else:
        page = int(page)

    start = (page - 1) * 10
    end = page * 10

    return start, end

# 版本信息数据列表 
def get_version_list(page, deviceType):
    # 获取查询页码
    start,end = getPage(page)
    logger.info("start:%s, end:%s"%(start,end))

    version_list = []
    total_num = 0

    if deviceType == "all":
        result = DevVerInfo.objects.all()[start:end]
        total_num = DevVerInfo.objects.all().count()
    else:
        result = DevVerInfo.objects.filter(device_type=deviceType)[start:end]
        total_num = DevVerInfo.objects.filter(device_type=deviceType).count()

    for version in result:
        version_list.append({'ver_sn': version.ver_sn,
                             'oem_mark': version.oem_mark,
                             'device_type': version.device_type,
                             'ver_level': version.ver_level,
                             'release_attribute': version.release_attribute,
                             'soft_ver': version.soft_ver,
                             'release_notes': version.release_notes,
                             'file_name': version.file_name,
                             'file_size': version.file_size, 
                             'grayrange_moidlist': version.grayrange_moidlist,
                             'grayrange_e164list': version.grayrange_e164list,
                             'file_md5': version.file_md5})
    return version_list, total_num

# 单个版本信息
class DevVerinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevVerInfo
        fields = ('ver_sn', 'oem_mark', 'device_type', 'ver_level', 'release_attribute', 'soft_ver', 'release_notes', 'file_name', 'file_size', 'grayrange_moidlist', 'grayrange_e164list', 'file_md5')

def save_version_info(oem_mark, device_type, ver_level, release_attribute, soft_ver, release_notes, file_name, file_size, grayrange_moidlist, grayrange_e164list, md5):
    ver_count = DevVerInfo.objects.filter(device_type=device_type,
                                          release_attribute=release_attribute).count()
    if ver_count > 0:
        return False
    devverinfo = DevVerInfo()
    # 赋值
    devverinfo.oem_mark = oem_mark
    devverinfo.device_type = device_type
    devverinfo.ver_level = ver_level
    devverinfo.release_attribute = release_attribute
    devverinfo.soft_ver = soft_ver
    devverinfo.release_notes = release_notes
    devverinfo.file_name = file_name
    devverinfo.file_size = file_size
    devverinfo.grayrange_moidlist = grayrange_moidlist
    devverinfo.grayrange_e164list = grayrange_e164list
    devverinfo.file_md5 = md5
    devverinfo.save()
    return True

def edit_verinfo(ver_sn, ver_level, release_attribute, release_notes, grayrange_moidlist, grayrange_e164list, tip):
    try:
        # 查询版本信息
        devverinfo = DevVerInfo.objects.get(ver_sn=ver_sn)

        # 查询版本数量,每个版本类型最多只能保存一个
        ver_count = DevVerInfo.objects.filter(device_type=devverinfo.device_type, release_attribute=release_attribute).count()
        logger.info('version count:%s' % ver_count)
        logger.info('version tip:%s' % tip)
        if ver_count > 0 and tip == "false":
            return 2
        else:
            # 保存修改
            devverinfo.ver_level = ver_level
            devverinfo.release_attribute = release_attribute
            devverinfo.release_notes = release_notes
            devverinfo.grayrange_moidlist = grayrange_moidlist
            devverinfo.grayrange_e164list = grayrange_e164list
            devverinfo.save()
            return 1
    except Exception as e:
        logger.error(e)
        return 0

def delete_version(ver_sn):
    # 查询
    devverinfo = DevVerInfo.objects.get(ver_sn=ver_sn)
    device_type = devverinfo.device_type
    soft_ver = devverinfo.soft_ver
    oem_mark = devverinfo.oem_mark
    devverinfo.delete()

    return oem_mark, device_type, soft_ver

def exist_verinfo(device_type, oem_mark, soft_ver):
    return DevVerInfo.objects.filter(oem_mark=oem_mark, device_type=device_type, soft_ver=soft_ver).count()

def filter_ver_info_list(oemmark_list, ver_list):
    result = DevVerInfo.objects.filter(oem_mark__in=oemmark_list, release_attribute__in=ver_list)
    ver_info_list = []
    for value in result:
        ver_info_list.append({'ver_sn': value.ver_sn,
                              'oem_mark': value.oem_mark,
                              'device_type': value.device_type,
                              'ver_level': value.ver_level,
                              'release_attribute': value.release_attribute,
                              'soft_ver': value.soft_ver,
                              'release_notes': value.release_notes,
                              'file_name': value.file_name,
                              'file_size': value.file_size,
                              'file_md5': value.file_md5,
                              'grayrange_moidlist': value.grayrange_moidlist,
                              'grayrange_e164list': value.grayrange_e164list})
    return ver_info_list