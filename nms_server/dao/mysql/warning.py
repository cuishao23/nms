from django.db import models

#服务器已修复告警表
class ServerWarningRepaired(models.Model):
    device_moid = models.CharField(max_length=40, blank=False)
    device_name = models.CharField(max_length=128, blank=True, null=True)
    device_type = models.CharField(max_length=36, blank=False)
    device_ip = models.CharField(max_length=128, blank=True, null=True)
    machine_room_moid = models.CharField(max_length=40,blank=False)
    machine_room_name = models.CharField(max_length=128, blank=True, null=True)
    code = models.SmallIntegerField(null=False)
    level = models.CharField(max_length=9,blank=False)
    description = models.CharField(max_length=128, blank=True, null=True)
    start_time = models.DateTimeField(null=False)
    resolve_time = models.DateTimeField(null=False)
    server_type = models.SmallIntegerField(null=False, default=0)

    class Meta:
        db_table = 'server_warning_repaired'
        app_label = 'warning'

#服务器未修复告警表
class ServerWarningUnrepaired(models.Model):
    device_moid = models.CharField(max_length=40, blank=False)
    device_name = models.CharField(max_length=128, blank=True, null=True)
    device_type = models.CharField(max_length=36, blank=False)
    device_ip = models.CharField(max_length=128, blank=True, null=True)
    machine_room_moid = models.CharField(max_length=40, blank=False)
    machine_room_name = models.CharField(max_length=128, blank=True, null=True)
    code = models.SmallIntegerField(null=False)
    level = models.CharField(max_length=9,blank=False)
    description = models.CharField(max_length=128, blank=True, null=True)
    start_time = models.DateTimeField(null=False)
    resolve_time = models.DateTimeField(null=True)
    server_type = models.SmallIntegerField(null=False, default=0)

    class Meta:
        db_table = 'server_warning_unrepaired'
        app_label = 'warning'


#终端已修复告警表
class TerminalWarningRepaired(models.Model):
    device_moid = models.CharField(max_length=40, blank=False)
    device_name = models.CharField(max_length=128, blank=True, null=True)
    device_type = models.CharField(max_length=36, blank=False)
    device_ip = models.CharField(max_length=128, blank=True, null=True)
    device_e164 = models.CharField(max_length=32, blank=True, null=True)
    domain_moid = models.CharField(max_length=40, blank=False)
    domain_name = models.CharField(max_length=128, blank=True, null=True)
    code = models.SmallIntegerField(null=False)
    level = models.CharField(max_length=9,null=False)
    description = models.CharField(max_length=128, blank=True, null=True)
    start_time = models.DateTimeField(null=False)
    resolve_time = models.DateTimeField(null=False)

    class Meta:
        db_table = 'terminal_warning_repaired'
        app_label = 'warning'


#终端未修复告警表
class TerminalWarningUnrepaired(models.Model):
    device_moid = models.CharField(max_length=40, blank=False)
    device_name = models.CharField(max_length=128, blank=True, null=True)
    device_type = models.CharField(max_length=36, blank=False)
    device_ip = models.CharField(max_length=128, blank=True, null=True)
    device_e164 = models.CharField(max_length=32, blank=True, null=True)
    domain_moid = models.CharField(max_length=40, blank=False)
    domain_name = models.CharField(max_length=128, blank=True, null=True)
    code = models.SmallIntegerField(null=False)
    level = models.CharField(max_length=9,null=False)
    description = models.CharField(max_length=128, blank=True, null=True)
    start_time = models.DateTimeField(null=False)
    resolve_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'terminal_warning_unrepaired'
        app_label = 'warning'


#告警码表
class WarningCode(models.Model):
    type = models.CharField(max_length=64, blank=False)
    code = models.SmallIntegerField(unique=True, null=False)
    name = models.CharField(max_length=128, blank=False)
    level = models.CharField(max_length=16, blank=False)
    description = models.CharField(max_length=128, blank=True, null=True)
    suggestion = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'warning_code'
        app_label = 'warning'


#基本信息页面告警显示级别表
class WarningLevelForBaseInfo(models.Model):
    domain_moid = models.CharField(max_length=40, blank=False)
    user_moid = models.CharField(max_length=40, blank=False)
    server_level = models.CharField(max_length=64, blank=False)
    terminal_level = models.CharField(max_length=64, blank=False)

    class Meta:
        db_table = 'warning_level_for_base_info'
        app_label = 'warning'

#老终端已修复告警表
class OldTerminalWarningRepaired(models.Model):
    moid = models.CharField(max_length=40, blank=False)
    device_name = models.CharField(max_length=128, blank=True, null=True)
    device_type = models.CharField(max_length=36, blank=False)
    device_ip = models.CharField(max_length=128, blank=True, null=True)
    code = models.SmallIntegerField(null=False)
    level = models.CharField(max_length=9, null=False)
    description = models.CharField(max_length=128, blank=True, null=True)
    start_time = models.DateTimeField(null=False)
    resolve_time = models.DateTimeField(null=False)

    class Meta:
        db_table = 'old_terminal_warning_repaired'
        app_label = 'warning'

#老终端未修复告警表
class OldTerminalWarningUnrepaired(models.Model):
    moid = models.CharField(max_length=40, blank=False)
    device_name = models.CharField(max_length=128, blank=True, null=True)
    device_type = models.CharField(max_length=36, blank=False)
    device_ip = models.CharField(max_length=128, blank=True, null=True)
    code = models.SmallIntegerField(null=False)
    level = models.CharField(max_length=9,null=False)
    description = models.CharField(max_length=128, blank=True, null=True)
    start_time = models.DateTimeField(null=False)
    resolve_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'old_terminal_warning_unrepaired'
        app_label = 'warning'