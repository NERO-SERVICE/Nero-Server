from rest_framework import serializers
from .models import YearlyDoseLog, YearlySideEffectLog

class YearlyDoseLogSerializer(serializers.ModelSerializer):
    dateIndex = serializers.SerializerMethodField()
    weekIndex = serializers.SerializerMethodField()

    class Meta:
        model = YearlyDoseLog
        fields = ['date', 'doseAction', 'dateIndex', 'weekIndex']

    def get_dateIndex(self, obj):
        # 요일을 반환 (월요일=0, 일요일=6)
        return obj.date.weekday()

    def get_weekIndex(self, obj):
        # 해당 연도의 몇 번째 주인지를 반환
        return obj.date.isocalendar()[1]  # (연도, 주, 요일)에서 주 값 반환

class YearlySideEffectLogSerializer(serializers.ModelSerializer):
    dateIndex = serializers.SerializerMethodField()
    weekIndex = serializers.SerializerMethodField()

    class Meta:
        model = YearlySideEffectLog
        fields = ['date', 'sideEffectAction', 'dateIndex', 'weekIndex']

    def get_dateIndex(self, obj):
        return obj.date.weekday()

    def get_weekIndex(self, obj):
        return obj.date.isocalendar()[1]
