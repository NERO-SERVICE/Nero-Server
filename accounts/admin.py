from django.contrib import admin
from accounts.models import User, Memories
from notification.models import Notification, ImageFile
from information.models import Information, InformationImageFile
from magazine.models import Magazine, MagazineImageFile
from mail.models import Mail
from django.utils import timezone 

# 사용자 관리
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'kakaoId', 'nickname', 'email', 'createdAt', 'birth', 'sex', 'is_product_writer', 'deleted_at']
    search_fields = ['nickname', 'email']
    readonly_fields = ['id', 'createdAt']
    list_filter = ['deleted_at', 'is_product_writer']
    actions = ['soft_delete_users', 'restore_users']

    def get_queryset(self, request):
        return User.all_objects.all()

    def soft_delete_users(self, request, queryset):
        queryset.update(deleted_at=timezone.now())
        self.message_user(request, "선택한 사용자가 소프트 삭제되었습니다.")
    soft_delete_users.short_description = "소프트 삭제 선택된 사용자"

    def restore_users(self, request, queryset):
        queryset.update(deleted_at=None)
        self.message_user(request, "선택한 사용자가 복원되었습니다.")
    restore_users.short_description = "선택된 사용자 복원"

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.deleted_at:
            return self.readonly_fields + ['nickname', 'email', 'sex', 'birth']
        return self.readonly_fields


@admin.register(Memories)
class MemoriesAdmin(admin.ModelAdmin):
    list_display = ['memoryId', 'get_user_nickname', 'items', 'deleted_at']
    search_fields = ['userId__nickname', 'items']
    readonly_fields = ['memoryId', 'deleted_at']

    def get_user_nickname(self, obj):
        return obj.userId.nickname

    get_user_nickname.short_description = '유저 닉네임'


# 공지사항 관리
class ImageFileInline(admin.TabularInline):
    model = ImageFile
    extra = 5
    fields = ['file', 'uploaded_at']
    readonly_fields = ['uploaded_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    inlines = [ImageFileInline]
    list_display = ('noticeId', 'title', 'writer', 'createdAt', 'updatedAt')
    search_fields = ('title', 'description', 'writer__nickname')
    readonly_fields = ('createdAt', 'updatedAt')

    fieldsets = (
        ('기본 정보', {'fields': ('title', 'description')}),
        ('작성자 정보', {'fields': ('writer',)}),
        ('추가 정보', {'fields': ('createdAt', 'updatedAt')}),
    )


# 개발자 공지 관리
class InformationImageFileInline(admin.TabularInline):
    model = InformationImageFile
    extra = 5
    fields = ['file', 'uploaded_at']
    readonly_fields = ['uploaded_at']

@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    inlines = [InformationImageFileInline]
    list_display = ('infoId', 'title', 'writer', 'createdAt', 'updatedAt')
    search_fields = ('title', 'description', 'writer__nickname')
    readonly_fields = ('createdAt', 'updatedAt')

    fieldsets = (
        ('기본 정보', {'fields': ('title', 'description')}),
        ('작성자 정보', {'fields': ('writer',)}),
        ('추가 정보', {'fields': ('createdAt', 'updatedAt')}),
    )


# 매거진 관리
class MagazineImageFileInline(admin.TabularInline):
    model = MagazineImageFile
    extra = 5
    fields = ['file', 'uploaded_at']
    readonly_fields = ['uploaded_at']

@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    inlines = [MagazineImageFileInline]
    list_display = ('magazineId', 'title', 'writer', 'createdAt', 'updatedAt')
    search_fields = ('title', 'description', 'writer__nickname')
    readonly_fields = ('createdAt', 'updatedAt')

    fieldsets = (
        ('기본 정보', {'fields': ('title', 'description')}),
        ('작성자 정보', {'fields': ('writer',)}),
        ('추가 정보', {'fields': ('createdAt', 'updatedAt')}),
    )


# 메일 관리
@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('owner', 'created_at', 'suggestion')
