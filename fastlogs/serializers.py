from rest_framework import serializers
from .models import DailyLog

class DailyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyLog
        fields = ['id', 'content', 'date']
        read_only_fields = ['id', 'date']

