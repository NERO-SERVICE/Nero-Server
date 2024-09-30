from django.contrib import admin
from .models import Clinics, Drug, DrugArchive, MyDrugArchive

@admin.register(Clinics)
class ClinicsAdmin(admin.ModelAdmin):
    list_display = ['clinicId', 'owner', 'recentDay', 'description', 'createdAt', 'updatedAt']
    search_fields = ['description', 'owner__username']
    list_filter = ['createdAt', 'updatedAt', 'owner']
    
    class Meta:
        app_label = "하루기록"
        verbose_name = "진료기록"
        verbose_name_plural = "진료기록"


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ['drugId', 'clinic', 'display_my_drug_archive_name', 'display_target', 'number', 'time', 'allow']
    search_fields = ['myDrugArchive__drugName', 'clinic__recentDay']
    list_filter = ['allow', 'time']
    
    def display_my_drug_archive_name(self, obj):
        return f"{obj.myDrugArchive.drugName} - {obj.myDrugArchive.capacity}mg"
    
    def display_target(self, obj):
        return obj.myDrugArchive.target
    
    display_my_drug_archive_name.short_description = 'Drug Name'
    display_target.short_description = 'Target'
    
    class Meta:
        app_label = "하루기록"
        verbose_name = "진료기록 - 약물 모음"
        verbose_name_plural = "진료기록 - 약물 모음"


@admin.register(DrugArchive)
class DrugArchiveAdmin(admin.ModelAdmin):
    list_display = ['archiveId', 'drugName', 'target', 'capacity']
    search_fields = ['drugName', 'target', 'capacity']
    list_filter = ['target']
    
    class Meta:
        app_label = "하루기록"
        verbose_name = "서버 저장 약물 아카이브"
        verbose_name_plural = "서버 저장 약물 아카이브"


@admin.register(MyDrugArchive)
class MyDrugArchiveAdmin(admin.ModelAdmin):
    list_display = ['myArchiveId', 'owner', 'archiveId', 'drugName', 'target', 'capacity']
    search_fields = ['owner__username', 'drugName']
    list_filter = ['target']
    
    class Meta:
        app_label = "하루기록"
        verbose_name = "진료기록 - 개별 약물"
        verbose_name_plural = "진료기록 - 개별 약물"
