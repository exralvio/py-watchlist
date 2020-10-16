from django.db import models
from datetime import datetime

class ActivityLogs(models.Model):
    user_id = models.IntegerField(null=False)
    ref = models.CharField(max_length=50, null=False)
    ref_id = models.IntegerField(null=False)
    action = models.CharField(max_length=50, null=False)
    note = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default=datetime.utcnow)

    class Meta:
        db_table = 'activity_logs'