from rest_framework import serializers
from .models import Today, Survey, SideEffect, SelfRecord

class TodaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Today
        fields = '__all__'

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'question', 'answer']

class SideEffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SideEffect
        fields = ['id', 'question', 'answer']

class SelfRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfRecord
        fields = ['id', 'created_at', 'content']

class TodayDetailSerializer(serializers.ModelSerializer):
    survey = SurveySerializer()
    side_effect = SideEffectSerializer()
    self_records = SelfRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Today
        fields = ['id', 'created_at', 'next_appointment_date', 'survey', 'side_effect', 'self_records']
