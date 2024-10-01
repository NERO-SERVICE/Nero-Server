from rest_framework import serializers
from .models import Today, SurveyResponse, SideEffectResponse, SelfRecord, Question, AnswerChoice

class TodaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Today
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'question_subtype']


class AnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = ['id', 'answer_code', 'answer_text']


class SurveyResponseSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    answer = AnswerChoiceSerializer(read_only=True)

    class Meta:
        model = SurveyResponse
        fields = ['id', 'question', 'answer', 'created_at']


class SideEffectResponseSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    answer = AnswerChoiceSerializer(read_only=True)

    class Meta:
        model = SideEffectResponse
        fields = ['id', 'question', 'answer', 'created_at']


class SelfRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfRecord
        fields = ['id', 'created_at', 'content']


class TodayDetailSerializer(serializers.ModelSerializer):
    survey_responses = SurveyResponseSerializer(many=True, read_only=True)
    side_effect_responses = SideEffectResponseSerializer(many=True, read_only=True)
    self_records = SelfRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Today
        fields = ['id', 'created_at', 'next_appointment_date', 'survey_responses', 'side_effect_responses', 'self_records']
