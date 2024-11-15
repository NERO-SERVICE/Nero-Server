from rest_framework import serializers
from .models import Menstruation

class MenstruationSerializer(serializers.ModelSerializer):
    startDate = serializers.DateField(
        input_formats=['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%S.%f']
    )
    endDate = serializers.DateField(
        input_formats=['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%S.%f']
    )
    cycleLength = serializers.SerializerMethodField()

    class Meta:
        model = Menstruation
        fields = ['id', 'owner', 'startDate', 'endDate', 'cycleLength', 'notes']
        read_only_fields = ['id', 'owner', 'cycleLength']

    def get_cycleLength(self, obj):
        return (obj.endDate - obj.startDate).days if obj.startDate and obj.endDate else None

    def validate(self, data):
        start_date = data.get('startDate')
        end_date = data.get('endDate')

        if end_date < start_date:
            raise serializers.ValidationError("종료일은 시작일보다 이후여야 합니다.")

        return data