from django.contrib import admin
from .models import DrfClinics, DrfDrug

@admin.register(DrfClinics)
class DrfClinicsAdmin(admin.ModelAdmin):
    list_display = ['clinicId', 'owner', 'title', 'createdAt', 'updatedAt']

@admin.register(DrfDrug)
class DrfDrugAdmin(admin.ModelAdmin):
    list_display = ['drugId', 'item', 'status', 'number']
