from django.contrib import admin
from .models import DrfProduct

class DrfProductAdmin(admin.ModelAdmin):
    # 관리자 페이지에서 보일 필드 목록
    list_display = ('title', 'owner', 'productPrice', 'status', 'categoryType', 'createdAt', 'updatedAt', 'viewCount')
    
    # 검색 기능을 제공할 필드
    search_fields = ('title', 'description', 'owner__username', 'status', 'categoryType')
    
    # 필터 기능을 제공할 필드
    list_filter = ('status', 'isFree', 'categoryType', 'createdAt', 'updatedAt')
    
    # 읽기 전용 필드
    readonly_fields = ('createdAt', 'updatedAt', 'viewCount', 'docId')

    # 상세 페이지에서 보일 필드 그룹화
    fieldsets = (
        ('Basic Information', {
            'fields': ('docId', 'title', 'description', 'productPrice', 'isFree', 'status', 'categoryType', 'image_urls')
        }),
        ('Owner Information', {
            'fields': ('owner',)
        }),
        ('Location Information', {
            'fields': ('wantTradeLocation', 'wantTradeLocationLabel')
        }),
        ('Additional Information', {
            'fields': ('viewCount', 'likers', 'createdAt', 'updatedAt')
        }),
    )

admin.site.register(DrfProduct, DrfProductAdmin)
