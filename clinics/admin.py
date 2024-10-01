from django.contrib import admin
from .models import Clinics, Drug, DrugArchive, MyDrugArchive

@admin.register(Clinics)
class ClinicsAdmin(admin.ModelAdmin):
    list_display = ['clinicId', 'owner', 'recentDay', 'description', 'createdAt', 'updatedAt']
    search_fields = ['description', 'owner__username']
    list_filter = ['createdAt', 'updatedAt', 'owner']


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ['drugId', 'clinic', 'display_my_drug_archive_name', 'display_target', 'number', 'time', 'allow']
    search_fields = ['myDrugArchive__archive__drugName', 'clinic__recentDay']
    list_filter = ['allow', 'time']
    
    def display_my_drug_archive_name(self, obj):
        return f"{obj.myDrugArchive.archive.drugName} - {obj.myDrugArchive.archive.capacity}mg"
    
    def display_target(self, obj):
        return obj.myDrugArchive.archive.target
    
    display_my_drug_archive_name.short_description = 'Drug Name'
    display_target.short_description = 'Target'


@admin.register(DrugArchive)
class DrugArchiveAdmin(admin.ModelAdmin):
    list_display = ['archiveId', 'drugName', 'target', 'capacity']
    search_fields = ['drugName', 'target', 'capacity']
    list_filter = ['target']


@admin.register(MyDrugArchive)
class MyDrugArchiveAdmin(admin.ModelAdmin):
    list_display = ['myArchiveId', 'owner', 'get_archive_id', 'get_drug_name', 'get_target', 'get_capacity']
    search_fields = ['owner__username', 'archive__drugName']
    list_filter = ['archive__target']
    
    def get_archive_id(self, obj):
        return obj.archive.archiveId
    
    def get_drug_name(self, obj):
        return obj.archive.drugName
    
    def get_target(self, obj):
        return obj.archive.target
    
    def get_capacity(self, obj):
        return obj.archive.capacity
    
    get_archive_id.short_description = 'Archive ID'
    get_drug_name.short_description = 'Drug Name'
    get_target.short_description = 'Target'
    get_capacity.short_description = 'Capacity'
