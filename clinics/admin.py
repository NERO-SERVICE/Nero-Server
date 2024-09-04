from django.contrib import admin
from .models import DrfClinics, DrfDrug, DrfDrugArchive

@admin.register(DrfClinics)
class DrfClinicsAdmin(admin.ModelAdmin):
    list_display = ['clinicId', 'owner', 'title', 'description', 'createdAt', 'updatedAt']
    search_fields = ['title', 'description', 'owner__username']

@admin.register(DrfDrug)
class DrfDrugAdmin(admin.ModelAdmin):
    list_display = ['drugId', 'item', 'display_drug_archives', 'number']
    search_fields = ['drugArchive__drugName', 'item__title']
    
    def display_drug_archives(self, obj):
        return ', '.join([archive.drugName for archive in obj.drugArchive.all()])
    
    display_drug_archives.short_description = 'Drug Archives'

@admin.register(DrfDrugArchive)
class DrfDrugArchiveAdmin(admin.ModelAdmin):
    list_display = ['id', 'drugName', 'target', 'capacity']
    search_fields = ['drugName', 'target', 'capacity']
