from rest_framework import serializers
from .models import Menstruation

class MenstruationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menstruation
        fields = ['id', 'owner', 'startDate', 'endDate', 'cycleLength', 'notes']
        read_only_fields = ['id', 'owner', 'cycleLength']
