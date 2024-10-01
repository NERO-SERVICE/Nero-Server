from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import YearlyLog
from todaylogs.models import SurveyCompletion

@receiver(post_save, sender=SurveyCompletion)
def create_yearly_log(sender, instance, created, **kwargs):
    if created and instance.response_type == 'side_effect':
        today_entry = instance.today
        user = today_entry.owner
        log_date = today_entry.created_at.date()
        
        # YearlyLog가 이미 존재하는지 확인
        log, created_log = YearlyLog.objects.get_or_create(
            owner=user,
            date=log_date,
            log_type='side_effect',
            defaults={'action': True}
        )
        
        if not created_log:
            # 이미 존재하는 경우, action 값을 업데이트할 수 있습니다.
            log.action = True
            log.save()