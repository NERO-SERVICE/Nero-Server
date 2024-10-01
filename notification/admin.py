from django.contrib import admin
from .models import Notification, ImageFile

class ImageFileInline(admin.TabularInline):
    model = ImageFile
    extra = 1
    fields = ['file', 'uploaded_at']
    readonly_fields = ['uploaded_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    inlines = [ImageFileInline]
    list_display = ('id', 'title', 'writer', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'writer__nickname')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Writer Information', {
            'fields': ('writer',)
        }),
        ('Additional Information', {
            'fields': ('created_at', 'updated_at')
        }),
    )

admin.site.register(ImageFile)
