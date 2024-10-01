from rest_framework import serializers
from .models import YearlyLog

class YearlyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearlyLog
        fields = ['owner', 'date', 'log_type', 'action']
        read_only_fields = ['owner']
