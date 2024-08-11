from django.contrib import admin
from .models import DrfProduct, ImageFile

class ImageFileInline(admin.TabularInline):
    model = ImageFile
    extra = 1
    fields = ['file', 'uploaded_at']
    readonly_fields = ['uploaded_at']


class DrfProductAdmin(admin.ModelAdmin):
    inlines = [ImageFileInline]
    list_display = ('id', 'title', 'owner', 'productPrice', 'status', 'categoryType', 'createdAt', 'updatedAt', 'viewCount')
    search_fields = ('title', 'description', 'owner__username', 'status', 'categoryType')
    list_filter = ('status', 'isFree', 'categoryType', 'createdAt', 'updatedAt')
    readonly_fields = ('createdAt', 'updatedAt', 'viewCount')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'productPrice', 'isFree', 'status', 'categoryType')
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
admin.site.register(ImageFile)