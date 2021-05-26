from django.db import models

#老终端表
class OldTerminal(models.Model):
    user_domain_moid = models.CharField(max_length=40, blank=False)
    moid = models.CharField(max_length=40, unique=True, blank=False)
    type = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    e164 = models.CharField(max_length=32, blank=True, null=True)
    ip = models.CharField(max_length=512, blank=False)
    online = models.CharField(max_length=1)
    version = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'old_terminal'
        app_label = 'device'