from django.db import models


# 多点会议历史统计
class MultiMeetingStatistic(models.Model):
    meeting_moid = models.CharField(max_length=40, blank = False)
    domain_moid = models.CharField(max_length=40, blank = False)
    conf_name = models.CharField(max_length=128, blank=True, null=True)
    conf_e164 = models.CharField(max_length=32, blank=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    info = models.TextField(blank=False)
    class Meta:
        app_label = 'meeting'
        db_table = 'multi_meeting_statistic'


# 参会IPC终端信息
class IpcMeetingStatistic(models.Model):
    meeting_moid = models.CharField(max_length=40, blank = False)
    info = models.TextField(blank=False)

    class Meta:
        app_label = 'meeting'
        db_table = 'ipc_meeting_statistic'


# 数据会议模式更改记录
class DcsModeChangeRecode(models.Model):
    dcs_moid = models.CharField(max_length=40, blank = False)
    info = models.TextField(blank=False)

    class Meta:
        app_label = 'meeting'
        db_table = 'dcs_mode_change_recode'

# 点对点会议历史统计
class P2PMeetingStatistic(models.Model):
    caller_name = models.CharField(max_length=128)
    caller_e164 = models.CharField(max_length=32)
    domain_moid = models.CharField(max_length=40, blank = False)
    meeting_moid = models.CharField(max_length=40, blank = False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    info = models.TextField(blank=False)

    class Meta:
        app_label = 'meeting'
        db_table = 'p2p_meeting_statistic'


# 参会IP或友商信息
class IpE164MeetingStatistic(models.Model):
    meeting_moid = models.CharField(max_length=40, blank = False)
    info = models.TextField(blank=False)

    class Meta:
        app_label = 'meeting'
        db_table = 'ip_e164_meeting_statistic'


# 直播信息
class LiveInfo(models.Model):
    meeting_moid = models.CharField(max_length=40, blank = False)
    info = models.TextField(blank=False)

    class Meta:
        app_label = 'meeting'
        db_table = 'live_info'


# 直播观看用户表
class UserInfoForLive(models.Model):
    live_moid = models.CharField(max_length=40, blank = False)
    info = models.TextField(blank=False)

    class Meta:
        app_label = 'meeting'
        db_table = 'user_info_for_live'

# 数据会议信息
class MeetingDcsInfo(models.Model):
    meeting_moid = models.CharField(max_length=40, blank = False)
    info = models.TextField(blank=False)

    class Meta:
        app_label = 'meeting'
        db_table = 'meeting_dcs_info'


# 上下级会议信息统计
class MeetingMeetingStatistic(models.Model):
    meeting_moid = models.CharField(max_length=40, blank = False)
    info = models.TextField(blank=False)

    class Meta:
        app_label = 'meeting'
        db_table = 'meeting_meeting_statistic'


# 会议终端详情历史统计
class MeetingTerminalDetailStatistic(models.Model):
    meeting_moid = models.CharField(max_length=40, blank = False)
    info = models.TextField(blank=False)

    class Meta:
        app_label = 'meeting'
        db_table = 'meeting_terminal_detail_statistic'

# 参会电话信息
class TelMeetingStatistic(models.Model):
    meeting_moid = models.CharField(max_length=40, blank = False)
    info = models.TextField(blank=False)

    class Meta:
        app_label = 'meeting'
        db_table = 'tel_meeting_statistic'


# 数据会议里的终端信息
class TerminalInfoForDcs(models.Model):
    dcs_moid = models.CharField(max_length=40, blank = False)
    info = models.TextField(blank=False)

    class Meta:
        app_label = 'meeting'
        db_table = 'terminal_info_for_dcs'


# 终端离会原因统计
class TerminalLeaveMeetingReason(models.Model):
    moid = models.CharField(max_length=40, blank = False)
    meeting_moid = models.CharField(max_length=40, blank = False)
    info = models.TextField(blank = False)

    class Meta:
        app_label = 'meeting'
        db_table = 'terminal_leave_meeting_reason'


# 终端参会概况
class TerminalMeetingScore(models.Model):
    meeting_moid = models.CharField(max_length=40)
    moid = models.CharField(max_length=40)
    info = models.TextField()

    class Meta:
        app_label = 'meeting'
        db_table = 'terminal_meeting_score'


# 会终端辅视屏信息
class TerminalMeetingAssvideo(models.Model):
    moid = models.CharField(max_length=40, blank = False)
    meeting_moid = models.CharField(max_length=40, blank = False)
    channel_id = models.SmallIntegerField(null=False)
    info = models.TextField(blank = False)

    class Meta:
        app_label = 'meeting'
        db_table = 'terminal_meeting_assvideo'


# 入会终端主视屏信息
class TerminalMeetingPrivideo(models.Model):
    moid = models.CharField(max_length=40, blank = False)
    meeting_moid = models.CharField(max_length=40, blank = False)
    channel_id = models.SmallIntegerField(null=False)
    info = models.TextField(blank = False)

    class Meta:
        app_label = 'meeting'
        db_table = 'terminal_meeting_privideo'

# 实体会议历史统计
class EntityMeetingStatistic(models.Model):
    domain_moid = models.CharField(max_length=40, blank = False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    info = models.TextField(blank=False)
    class Meta:
        app_label = 'meeting'
        db_table = 'entity_meeting_statistic'