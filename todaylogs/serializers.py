from rest_framework import serializers
from .models import Today, Response, SelfRecord, Question, AnswerChoice

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


class ResponseSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    answer = AnswerChoiceSerializer(read_only=True)

    class Meta:
        model = Response
        fields = ['id', 'question', 'answer', 'created_at', 'response_type']


class SelfRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfRecord
        fields = ['id', 'created_at', 'content']


class TodayDetailSerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(many=True, read_only=True)
    self_records = SelfRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Today
        fields = ['id', 'created_at', 'next_appointment_date', 'responses', 'self_records']
