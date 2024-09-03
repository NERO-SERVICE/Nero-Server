from django.contrib import admin
from .models import DrfClinics, DrfDrug, DrfDrugArchive

@admin.register(DrfClinics)
class DrfClinicsAdmin(admin.ModelAdmin):
    list_display = ['clinicId', 'owner', 'title', 'description', 'createdAt', 'updatedAt']

@admin.register(DrfDrug)
class DrfDrugAdmin(admin.ModelAdmin):
    list_display = ['drugId', 'item', 'drugArchive', 'number']
    search_fields = ['drugArchive__drugName']

@admin.register(DrfDrugArchive)
class DrfDrugArchiveAdmin(admin.ModelAdmin):
    list_display = ['id', 'drugName', 'target', 'capacity']
    search_fields = ['drugName']
