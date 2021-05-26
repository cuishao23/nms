from django.db import models
from rest_framework import serializers

LEVEL_CHOICES = (
    ("critical", "严重告警"),
    ("important", "重要告警"),
    ("normal", "一般告警"),
    ("none", "正常")
)


class InspectTask(models.Model):
    domain_moid = models.CharField(max_length=40, blank=False)
    user_moid = models.CharField(max_length=40, blank=False)
    start_time = models.DateTimeField(null=False)
    license = models.IntegerField(null=False)
    resource = models.IntegerField(null=False)
    server = models.IntegerField(null=False)
    terminal = models.IntegerField(null=False)
    recycle = models.IntegerField(null=False)
    executed = models.IntegerField(null=False, default=0)
    sub_task = models.IntegerField(blank=False, default=0)
    parent_task = models.IntegerField(blank=True, null=True)
    task_flag = models.IntegerField(blank=False, default=0)

    class Meta:
        db_table = 'inspect_task'
        app_label = 'diagnosis'
        verbose_name = '巡检任务表'


class InspectRange(models.Model):
    taskid = models.ForeignKey(
        'InspectTask', models.DO_NOTHING, db_column='taskid')
    inspect_type = models.CharField(max_length=8, blank=False)
    service_domain_moid = models.CharField(max_length=40, default='all')
    platform_domain_moid = models.CharField(max_length=40, default='all')
    virtual_machine_room_moid = models.CharField(max_length=40, default='all')
    user_domain_moid = models.CharField(max_length=40, default='all')

    class Meta:
        db_table = 'inspect_range'
        app_label = 'diagnosis'
        verbose_name = '巡检范围'


class InspectRecycle(models.Model):
    taskid = models.ForeignKey(
        'InspectTask', models.DO_NOTHING, db_column='taskid')
    end_time = models.DateTimeField(blank=True, null=True)
    monday = models.IntegerField(null=False)
    tuesday = models.IntegerField(null=False)
    wednesday = models.IntegerField(null=False)
    thursday = models.IntegerField(null=False)
    friday = models.IntegerField(null=False)
    saturday = models.IntegerField(null=False)
    sunday = models.IntegerField(null=False)

    class Meta:
        db_table = 'inspect_recycle'
        app_label = 'diagnosis'
        verbose_name = '定时巡检表'


class InspectLicenseResult(models.Model):
    LICENSE_CHOICES = (
        ("normal", "正常"),
        ("expired", "过期")
    )
    taskid = models.IntegerField(null=False)
    auth_id = models.CharField(max_length=128, blank=False)
    auth_dead_time = models.DateTimeField(null=False)
    auth_status = models.CharField(
        max_length=7, blank=False, choices=LICENSE_CHOICES)
    service_domain_moid = models.CharField(max_length=40, blank=False)
    service_domain_name = models.CharField(max_length=128, blank=False)

    @property
    def auth_status_display(self):
        return self.get_auth_status_display()

    class Meta:
        db_table = 'inspect_license_result'
        app_label = 'diagnosis'
        verbose_name = '许可证巡检结果'


class InspectResourceResult(models.Model):
    taskid = models.IntegerField(null=False)
    resource_json = models.TextField(null=False)

    class Meta:
        db_table = 'inspect_resource_result'
        app_label = 'diagnosis'
        verbose_name = '资源巡检结果'


class InspectServerResult(models.Model):
    taskid = models.IntegerField(null=False)
    device_name = models.CharField(max_length=128, blank=False)
    device_moid = models.CharField(max_length=40, blank=False)
    device_ip = models.CharField(max_length=512, default='')
    device_type = models.CharField(max_length=32, blank=False)
    server_type = models.CharField(max_length=8, blank=False)
    level = models.CharField(max_length=9, blank=False,
                             default='none', choices=LEVEL_CHOICES)
    online = models.CharField(max_length=10, blank=False)
    machine_room_moid = models.CharField(max_length=40, blank=False)
    machine_room_name = models.CharField(max_length=128, blank=False)

    @property
    def level_display(self):
        return self.get_level_display()

    class Meta:
        db_table = 'inspect_server_result'
        app_label = 'diagnosis'
        verbose_name = '服务器巡检结果'


class InspectServerHwResult(models.Model):
    taskid = models.IntegerField(null=False)
    device_moid = models.CharField(max_length=40, blank=False)
    hw_json = models.TextField(null=False)

    class Meta:
        db_table = 'inspect_server_hw_result'
        app_label = 'diagnosis'
        verbose_name = '服务器硬件状态巡检结果'


class InspectServerUnrepairedWarnning(models.Model):
    taskid = models.IntegerField(null=False)
    device_moid = models.CharField(max_length=40, blank=False)
    level = models.CharField(max_length=9, blank=False, choices=LEVEL_CHOICES)
    code = models.SmallIntegerField(null=False)
    start_time = models.DateTimeField(null=False)
    description = models.CharField(max_length=128, blank=False)

    @property
    def level_display(self):
        return self.get_level_display()

    class Meta:
        db_table = 'inspect_server_unrepaired_warnning'
        app_label = 'diagnosis'
        verbose_name = '服务器未修复告警巡检表'


class InspectTerminalResult(models.Model):
    taskid = models.IntegerField(null=False)
    device_name = models.CharField(max_length=128, blank=False)
    device_moid = models.CharField(max_length=40, blank=False)
    device_type = models.CharField(max_length=32, blank=False)
    device_ip = models.CharField(max_length=512)
    e164 = models.CharField(max_length=32, blank=False)
    level = models.CharField(max_length=9, blank=False, choices=LEVEL_CHOICES)
    user_domain_moid = models.CharField(max_length=40, blank=False)
    user_domain_name = models.CharField(max_length=40, blank=False)

    @property
    def level_display(self):
        return self.get_level_display()

    class Meta:
        db_table = 'inspect_terminal_result'
        app_label = 'diagnosis'
        verbose_name = '终端巡检结果'


class InspectTerminalUnrepairedWarnning(models.Model):
    taskid = models.IntegerField(null=False)
    device_moid = models.CharField(max_length=40, blank=False)
    level = models.CharField(max_length=9, blank=False, choices=LEVEL_CHOICES)
    code = models.SmallIntegerField(null=False)
    start_time = models.DateTimeField(null=False)
    description = models.CharField(max_length=128, blank=False)

    @property
    def level_display(self):
        return self.get_level_display()

    class Meta:
        db_table = 'inspect_terminal_unrepaired_warnning'
        app_label = 'diagnosis'
        verbose_name = '终端未修复告警巡检表'


class InspectTaskSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = InspectTask
        exclude = []


class InspectRecycleSerializer(serializers.ModelSerializer):
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = InspectRecycle
        exclude = []


class InspectLicenseResultSerializer(serializers.ModelSerializer):
    auth_dead_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = InspectLicenseResult
        exclude = []


class InspectServerUnrepairedWarnningSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = InspectServerUnrepairedWarnning
        exclude = []


class InspectTerminalUnrepairedWarnningSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = InspectTerminalUnrepairedWarnning
        exclude = []
