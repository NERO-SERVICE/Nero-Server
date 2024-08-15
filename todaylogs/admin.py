from django.contrib import admin
from .models import Today, Survey, SideEffect, SelfRecord

admin.site.register(Today)
admin.site.register(Survey)
admin.site.register(SideEffect)
admin.site.register(SelfRecord)
