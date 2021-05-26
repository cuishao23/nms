from django.db import models

class StopWarning(models.Model):
    moid = models.CharField(max_length=40, unique=True, blank=False)

    class Meta:
        db_table = 'stop_warning'
        app_label = 'system_set'

#通用阈值设置数据表
class ResourceLimit(models.Model):
    s_pas = models.SmallIntegerField(null=True, default=5000)
    s_callpair = models.SmallIntegerField(null=True, default=400)
    s_nms = models.SmallIntegerField(null=True, default=10000)
    s_media_resource = models.SmallIntegerField(null=True, default=80)

    class Meta:
        db_table = 'resource_limit'
        app_label = 'system_set'

#服务器阈值设置数据表
class ServerResourceLimit(models.Model):
    device_moid = models.CharField(max_length=40, blank=False)
    cpu = models.SmallIntegerField(null=True, default=80)
    memory = models.SmallIntegerField(null=True, default=80)
    disk = models.SmallIntegerField(null=True, default=80)
    port = models.SmallIntegerField(null=True, default=60)
    diskwritespeed = models.SmallIntegerField(null=True, default=2)
    rateofflow = models.IntegerField(null=True, default=500)

    class Meta:
        db_table = 'server_resource_limit'
        app_label = 'system_set'

#订阅告警数据表
class SubWarningCode(models.Model):
    domain_moid = models.CharField(max_length=40, blank=False)
    user_id = models.CharField(max_length=40, blank=False)
    sub_code = models.SmallIntegerField(null=False)

    class Meta:
        db_table = 'sub_warning_code'
        app_label = 'system_set'


# 告警通知数据表
class WarningNotify(models.Model):
    domain_moid = models.CharField(max_length=40, blank=False)
    user_moid = models.CharField(max_length=40, blank=False)
    name = models.CharField(max_length=128, blank=False)
    code_list = models.CharField(max_length=1024, blank=False)
    email = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    wechat = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'warning_notify'
        app_label = 'system_set'

class TerminalType(models.Model):
    name = models.CharField(max_length=128, blank=False, verbose_name="设备主型号")
    terminal_type = models.CharField(max_length=2, blank=False, verbose_name="终端类型")
    device_tag = models.CharField(max_length=50, blank=False, verbose_name="登录验证标识")
    product_name = models.CharField(max_length=128, blank=False, verbose_name="设备子型号")
    platform_type = models.SmallIntegerField(null=True, default=2)

    class Meta:
        app_label = 'system_set'
        db_table = 'terminal_type'
        verbose_name = '设备型号数据列表'

class TerminalTypeLimit(models.Model):
    moid = models.CharField(max_length=40, blank=False, verbose_name="本条限制信息的唯一ID")
    e164 = models.CharField(max_length=32, blank=True, verbose_name="164号码限制")
    version = models.CharField(max_length=64, blank=True, verbose_name="版本号限制")
    sn = models.CharField(max_length=64, blank=True, verbose_name="Sn号限制(硬终端适用)")
    ip = models.CharField(max_length=64, blank=True, verbose_name="Ip限制")
    start_ip = models.CharField(max_length=64, blank=True, verbose_name="起始ip(ip段限制)")
    end_ip = models.CharField(max_length=64, blank=True, verbose_name="结束ip(ip段限制)")
    terminal_type = models.SmallIntegerField(null=True, verbose_name="终端类型 0:软,1:硬")
    main_type = models.CharField(max_length=128, blank=True, verbose_name="可登录设备 主型号")
    sub_type = models.CharField(max_length=128, blank=True, verbose_name="可登录设备 子型号")
    limit_type = models.SmallIntegerField(null=False, verbose_name="限制类型 0-黑名单;1-白名单")

    class Meta:
        app_label = 'system_set'
        db_table = 'terminal_type_limit'
        verbose_name = '终端型号限制表'

class TerminalTypeLimitCfg(models.Model):
    value = models.SmallIntegerField(null=False, verbose_name="0-关闭限制；1-黑名单生效；2-白名单生效")

    class Meta:
        app_label = 'system_set'
        db_table = 'terminal_type_limit_cfg'
        verbose_name = '终端型号限制配置表'