from django.contrib import admin
from .models import DrfProduct

class DrfProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'productPrice', 'status', 'categoryType', 'createdAt', 'updatedAt', 'viewCount')
    search_fields = ('title', 'description', 'owner__username', 'status', 'categoryType')
    list_filter = ('status', 'isFree', 'categoryType', 'createdAt', 'updatedAt')
    readonly_fields = ('createdAt', 'updatedAt', 'viewCount', 'docId')

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
