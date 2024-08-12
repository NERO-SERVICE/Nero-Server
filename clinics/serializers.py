from rest_framework import serializers
from .models import DrfClinics, DrfDrug

class DrfDrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrfDrug
        fields = ['drugId', 'status', 'number', 'time']

class DrfClinicsSerializer(serializers.ModelSerializer):
    drugs = DrfDrugSerializer(many=True, read_only=True)

    class Meta:
        model = DrfClinics
        fields = ['clinicId', 'owner', 'recentDay', 'nextDay', 'createdAt', 'updatedAt', 'title', 'drugs']
