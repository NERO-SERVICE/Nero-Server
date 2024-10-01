from django.apps import AppConfig


class MypageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mypage'
    verbose_name = '마이페이지'
    
    def ready(self):
        import mypage.signals
