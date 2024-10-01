from django.contrib import admin
from .models import Magazine, MagazineImageFile

class MagazineImageFileInline(admin.TabularInline):
    model = MagazineImageFile
    extra = 1
    fields = ['file', 'uploaded_at']
    readonly_fields = ['uploaded_at']

class MagazineAdmin(admin.ModelAdmin):
    inlines = [MagazineImageFileInline]
    list_display = ('magazineId', 'title', 'writer', 'createdAt', 'updatedAt')
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

admin.site.register(Magazine, MagazineAdmin)
admin.site.register(MagazineImageFile)
