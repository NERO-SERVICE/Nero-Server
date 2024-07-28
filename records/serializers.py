from rest_framework import serializers
from .models import QuestionList, ServeyLog, SymptomCare, SymptomLog

class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionList
        fields = ('questionId', 'type', 'content')

class ServeyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServeyLog
        fields = ('logId', 'questions', 'today', 'answer')

class SymptomCareSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomCare
        fields = ('symptomId', 'type', 'content')

class SymptomLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomLog
        fields = ('symptomLogId', 'symptomQuestions', 'today', 'answer')
