from django.core.management.base import BaseCommand
from django.utils import timezone
from clinics.models import Drug

class Command(BaseCommand):
    help = '매일 자정에 약물 상태를 갱신합니다.'

    def handle(self, *args, **options):
        now = timezone.now()
        self.stdout.write(f"약물 상태 갱신 시작: {now}")

        try:
            # 상태 갱신 로직 구현
            drugs_to_reset = Drug.objects.filter(allow=False)
            count = drugs_to_reset.update(allow=True)
            self.stdout.write(self.style.SUCCESS(f"성공적으로 {count}개의 약물 상태를 갱신했습니다."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"약물 상태 갱신 중 오류 발생: {e}"))