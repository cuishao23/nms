from django.db import models

class DevVerInfo(models.Model):
    ver_sn = models.AutoField(primary_key=True, blank=False, unique=True)
    oem_mark = models.CharField(max_length=32, blank=False, verbose_name="oem标识")
    device_type = models.CharField(max_length=64, blank=False, verbose_name="终端类型")
    ver_level = models.IntegerField(null=False, verbose_name="版本级别")
    release_attribute = models.IntegerField(null=False, verbose_name="版本属性")
    soft_ver = models.CharField(max_length=64, blank=False, verbose_name="版本号")
    release_notes = models.CharField(max_length=2048, blank=True, null=True, verbose_name="版本描述信息")
    file_name = models.CharField(max_length=64, blank=False, verbose_name="文件名")
    file_size = models.IntegerField(null=False, verbose_name="文件大小")
    grayrange_moidlist = models.CharField(max_length=2048, blank=True, null=True, verbose_name="用户域moid列表")
    grayrange_e164list = models.CharField(max_length=2048, blank=True, null=True, verbose_name="e164号码列表")
    file_md5 = models.CharField(max_length=48, blank=False, verbose_name="文件md5")

    class Meta:
        app_label = 'sus'
        db_table = 'dev_ver_info'
        verbose_name = '版本信息数据表'