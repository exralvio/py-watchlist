from .models import ActivityLogs
from WatchList.helpers import getUserID
from django.utils import timezone

def logger(user_id=None, ref=None, ref_id=None, action=None, note=None):
    # user_id, ref, ref_id and action is required
    if not user_id or not ref or not ref_id or not action:
        return

    log = ActivityLogs()
    log.user_id = user_id
    log.ref = ref
    log.ref_id = ref_id
    log.action = action
    log.note = note
    log.created_at = timezone.now()
    log.save()

    return
