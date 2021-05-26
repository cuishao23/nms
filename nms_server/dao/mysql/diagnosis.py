from django.db import models

# 抓包对象
class CaptureDevice(models.Model):
    user_moid = models.CharField(max_length=40, blank=False, verbose_name="用户moid")
    device_moid = models.CharField(max_length=40, blank=False, verbose_name="设备moid")
    device_ip = models.CharField(max_length=512, blank=False, verbose_name="设备ip")
    device_name = models.CharField(max_length=128, blank=False, verbose_name="设备名称")
    device_category = models.CharField(max_length=8, blank=False, verbose_name="设备类型")
    device_type = models.CharField(max_length=36, blank=False, verbose_name="设备型号")
    netcard = models.CharField(max_length=32, blank=False, verbose_name="抓包网口名")

    class Meta:
        app_label = 'diagnosis'
        db_table = 'capture_device'

# 抓包数据
class CaptureFile(models.Model):
    user_moid = models.CharField(max_length=40, blank=False, verbose_name="用户moid")
    device_moid = models.CharField(max_length=40, blank=False, verbose_name="设备moid")
    device_name = models.CharField(max_length=128, blank=False, verbose_name="设备名称")
    file_name = models.CharField(max_length=128, blank=False, verbose_name="抓包文件名")
    file_size = models.IntegerField(null=False, verbose_name="抓包文件大小")
    create_time = models.DateTimeField(null=False, verbose_name="文件生成时间")

    class Meta:
        app_label = 'diagnosis'
        db_table = 'capture_file'