from django.contrib import admin
from .models import Information, InformationImageFile

class InformationImageFileInline(admin.TabularInline):
    model = InformationImageFile
    extra = 5
    fields = ['file', 'uploaded_at']
    readonly_fields = ['uploaded_at']

class InformationAdmin(admin.ModelAdmin):
    inlines = [InformationImageFileInline]
    list_display = ('infoId', 'title', 'writer', 'createdAt', 'updatedAt')
    search_fields = ('title', 'description', 'writer__nickname')
    readonly_fields = ('createdAt', 'updatedAt')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Writer Information', {
            'fields': ('writer',)
        }),
        ('Additional Information', {
            'fields': ('createdAt', 'updatedAt')
        }),
    )
    
    class Meta:
        app_label = "유저관리"
        verbose_name = "개발자 공지"
        verbose_name_plural = "개발자 공지"

admin.site.register(Information, InformationAdmin)
admin.site.register(InformationImageFile)
