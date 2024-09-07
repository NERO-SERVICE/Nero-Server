from django.contrib import admin
from .models import DrfClinics, DrfDrug, DrfDrugArchive, DrfMyDrugArchive

@admin.register(DrfClinics)
class DrfClinicsAdmin(admin.ModelAdmin):
    list_display = ['clinicId', 'owner', 'title', 'description', 'createdAt', 'updatedAt']
    search_fields = ['title', 'description', 'owner__username']
    list_filter = ['createdAt', 'updatedAt', 'owner']

@admin.register(DrfDrug)
class DrfDrugAdmin(admin.ModelAdmin):
    list_display = ['drugId', 'clinic', 'display_my_drug_archive_name', 'display_target', 'number', 'time', 'allow']
    search_fields = ['myDrugArchive__drugName', 'clinic__title']
    list_filter = ['allow', 'time']
    
    def display_my_drug_archive_name(self, obj):
        return f"{obj.myDrugArchive.drugName} - {obj.myDrugArchive.capacity}mg"
    
    def display_target(self, obj):
        return obj.myDrugArchive.target
    
    display_my_drug_archive_name.short_description = 'Drug Name'
    display_target.short_description = 'Target'

@admin.register(DrfDrugArchive)
class DrfDrugArchiveAdmin(admin.ModelAdmin):
    list_display = ['archiveId', 'drugName', 'target', 'capacity']
    search_fields = ['drugName', 'target', 'capacity']
    list_filter = ['target']

@admin.register(DrfMyDrugArchive)
class DrfMyDrugArchiveAdmin(admin.ModelAdmin):
    list_display = ['myArchiveId', 'owner', 'archiveId', 'drugName', 'target', 'capacity']
    search_fields = ['owner__username', 'drugName']
    list_filter = ['target']
