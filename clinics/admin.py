from django.contrib import admin
from .models import DrfClinics, DrfDrug, DrfDrugArchive

@admin.register(DrfClinics)
class DrfClinicsAdmin(admin.ModelAdmin):
    list_display = ['clinicId', 'owner', 'title', 'description', 'createdAt', 'updatedAt']
    search_fields = ['title', 'description', 'owner__username']
    list_filter = ['createdAt', 'updatedAt', 'owner']

@admin.register(DrfDrug)
class DrfDrugAdmin(admin.ModelAdmin):
    list_display = ['drugId', 'clinic', 'display_drug_archive_name', 'number', 'time', 'allow']
    search_fields = ['drugArchive__drugName', 'clinic__title']
    list_filter = ['allow', 'time']

    def display_drug_archive_name(self, obj):
        return obj.drugArchive.drugName
    
    display_drug_archive_name.short_description = 'Drug Name'

@admin.register(DrfDrugArchive)
class DrfDrugArchiveAdmin(admin.ModelAdmin):
    list_display = ['id', 'drugName', 'target', 'capacity']
    search_fields = ['drugName', 'target', 'capacity']
    list_filter = ['target']
