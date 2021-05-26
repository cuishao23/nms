from django.db import models

class Log(models.Model):
    domain_moid = models.CharField(max_length=40, blank=False, verbose_name="域moid")
    user_moid = models.CharField(max_length=40, blank=False, verbose_name="用户域moid")
    user = models.CharField(max_length=128, blank=False, verbose_name="用户名")
    ip = models.CharField(max_length=512, blank=True, null=True, verbose_name="IP地址")
    time = models.DateTimeField(null=False, verbose_name="操作时间")
    type = models.CharField(max_length=13, blank=False, null=True, verbose_name="操作类型")
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name="操作描述")
    level = models.CharField(max_length=9, verbose_name="操作等级")
    result = models.CharField(max_length=7, verbose_name="操作结果")
    fail_reason = models.CharField(max_length=128, blank=True, null=True, verbose_name="失败原因")

    class Meta:
        db_table = 'log'
        app_label = 'opr_log'
        verbose_name = '网管操作日志'