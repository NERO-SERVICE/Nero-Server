from rest_framework import serializers
from .models import YearlyDoseLog, YearlySideEffectLog

class YearlyDoseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearlyDoseLog
        fields = ['owner', 'date', 'doseAction']

class YearlySideEffectLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearlySideEffectLog
        fields = ['owner', 'date', 'sideEffectAction']
