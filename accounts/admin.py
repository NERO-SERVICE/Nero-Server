from django.contrib import admin
from accounts.models import User, Memories
from notification.models import Notification, ImageFile
from information.models import Information, InformationImageFile
from magazine.models import Magazine, MagazineImageFile
from mail.models import Mail

# 유저관리
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'email', 'createdAt', 'birth', 'sex']
    search_fields = ['nickname', 'email']

    class Meta:
        app_label = "유저관리"
        verbose_name = "유저관리"
        verbose_name_plural = "유저관리"


@admin.register(Memories)
class MemoriesAdmin(admin.ModelAdmin):
    list_display = ['memoryId', 'userId', 'items']
    search_fields = ['userId', 'items']

    class Meta:
        app_label = "유저관리"
        verbose_name = "챙길거리"
        verbose_name_plural = "챙길거리"


# 공지
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['noticeId', 'title', 'writer', 'createdAt']
    search_fields = ['title']

    class Meta:
        app_label = "유저관리"
        verbose_name = "공지"
        verbose_name_plural = "공지"


# 개발자 공지
@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ['infoId', 'title', 'writer', 'createdAt']
    search_fields = ['title']

    class Meta:
        app_label = "유저관리"
        verbose_name = "개발자 공지"
        verbose_name_plural = "개발자 공지"


# 매거진
@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ['magazineId', 'title', 'writer', 'createdAt']
    search_fields = ['title']

    class Meta:
        app_label = "유저관리"
        verbose_name = "매거진"
        verbose_name_plural = "매거진"


# 메일
@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ['owner', 'created_at', 'suggestion']

    class Meta:
        app_label = "유저관리"
        verbose_name = "개발자 건의함"
        verbose_name_plural = "개발자 건의함"
