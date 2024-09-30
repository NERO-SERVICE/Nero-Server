from celery import shared_task
from django.utils import timezone
from pytz import timezone as pytz_timezone
from .models import Drug

@shared_task
def reset_drug_allow_flags():
    korea_tz = pytz_timezone('Asia/Seoul')
    now = timezone.now().astimezone(korea_tz)
    reset_time = now.replace(hour=0, minute=0, second=0, microsecond=0)

    if now >= reset_time:
        drugs_to_reset = Drug.objects.filter(allow=False)
        drugs_to_reset.update(allow=True)
        print(f"Reset allow flags at {now}")