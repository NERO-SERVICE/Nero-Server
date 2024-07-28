from rest_framework import serializers
from .models import DrugList, ClinicLog

class DrugListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugList
        fields = ('id', 'drugName', 'capacity', 'unit')

class ClinicLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicLog
        fields = ('clinicId', 'drug', 'user', 'location', 'clinicDate', 'nextDate', 'doseTime', 'clinicNote')