from rest_framework import serializers
from .models import Today, Response, SelfRecord, Question, AnswerChoice, QuestionSubtype, SurveyCompletion

class TodaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Today
        fields = '__all__'


class QuestionSubtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSubtype
        fields = ['id', 'subtype_code', 'subtype_name']


class AnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = ['id', 'answer_code', 'answer_text']


class QuestionSerializer(serializers.ModelSerializer):
    answer_choices = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'question_subtype', 'answer_choices']

    def get_answer_choices(self, obj):
        answer_choices = AnswerChoice.objects.filter(
            question_type=obj.question_type,
            question_subtype=obj.question_subtype
        )
        return AnswerChoiceSerializer(answer_choices, many=True).data        


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


class SurveyCompletionSerializer(serializers.ModelSerializer):
    question_subtype = QuestionSubtypeSerializer(read_only=True)

    class Meta:
        model = SurveyCompletion
        fields = ['id', 'response_type', 'question_subtype', 'completed_at']


class TodayDetailSerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(many=True, read_only=True)
    self_records = SelfRecordSerializer(many=True, read_only=True)
    survey_completions = SurveyCompletionSerializer(many=True, read_only=True)

    class Meta:
        model = Today
        fields = ['id', 'created_at', 'next_appointment_date', 'responses', 'self_records', 'survey_completions']


class TodayDetailSerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(many=True, read_only=True)
    self_records = SelfRecordSerializer(many=True, read_only=True)
    survey_completions = SurveyCompletionSerializer(many=True, read_only=True)

    class Meta:
        model = Today
        fields = ['id', 'created_at', 'next_appointment_date', 'responses', 'self_records', 'survey_completions']