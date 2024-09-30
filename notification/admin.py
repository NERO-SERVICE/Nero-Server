# from django.contrib import admin
# from .models import Notification, ImageFile

# class ImageFileInline(admin.TabularInline):
#     model = ImageFile
#     extra = 5
#     fields = ['file', 'uploaded_at']
#     readonly_fields = ['uploaded_at']


# class NotificationAdmin(admin.ModelAdmin):
#     inlines = [ImageFileInline]
#     list_display = ('noticeId', 'title', 'writer', 'createdAt', 'updatedAt')
#     search_fields = ('title', 'description', 'writer__nickname') 
#     readonly_fields = ('createdAt', 'updatedAt')

#     fieldsets = (
#         ('Basic Information', {
#             'fields': ('title', 'description')
#         }),
#         ('Writer Information', {
#             'fields': ('writer',)
#         }),
#         ('Additional Information', {
#             'fields': ('createdAt', 'updatedAt')
#         }),
#     )


# admin.site.register(Notification, NotificationAdmin)
# admin.site.register(ImageFile)
