from django.contrib import admin
from todaylogs.models import Today
from clinics.models import Clinics

# 하루기록
@admin.register(Today)
class TodayAdmin(admin.ModelAdmin):
    list_display = ['owner', 'date', 'content']

    class Meta:
        app_label = "하루기록"
        verbose_name = "하루기록"
        verbose_name_plural = "하루기록"


# 진료기록
@admin.register(Clinics)
class ClinicsAdmin(admin.ModelAdmin):
    list_display = ['clinicId', 'owner', 'recentDay', 'description']

    class Meta:
        app_label = "하루기록"
        verbose_name = "진료기록"
        verbose_name_plural = "진료기록"
