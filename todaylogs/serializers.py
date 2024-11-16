from rest_framework import serializers
from .models import Today, Response, SelfRecord, Question, AnswerChoice, QuestionSubtype, SurveyCompletion
from django.utils import timezone

class TodaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Today
        fields = '__all__'


class QuestionSubtypeSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = QuestionSubtype
        fields = ['subtype_code', 'subtype_name', 'is_completed']

    def get_is_completed(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        if user:
            today = Today.objects.filter(owner=user, created_at__date=timezone.localtime(timezone.now()).date()).first()
            response_type = self.context.get('response_type')
            if today and response_type:
                return SurveyCompletion.objects.filter(
                    today=today,
                    response_type=response_type,
                    question_subtype=obj
                ).exists()
        return False


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
        

class QuestionWithAnswerTextSerializer(serializers.Serializer):
    question_text = serializers.CharField()
    answer_text = serializers.CharField(allow_blank=True, required=False)

class SubtypeWithQuestionsSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = QuestionSubtype
        fields = ['subtype_code', 'subtype_name', 'questions']

    def get_questions(self, obj):
        today = self.context.get('today')
        response_type = self.context.get('response_type')
        
        # 해당 서브타입의 모든 질문 가져오기
        questions = obj.questions.all()
        question_data = []
        for question in questions:
            try:
                # 사용자의 응답 찾기
                response = Response.objects.get(
                    today=today,
                    question=question,
                    response_type=response_type
                )
                answer_text = response.answer.answer_text
            except Response.DoesNotExist:
                # 응답이 없는 경우 빈 문자열 또는 원하는 메시지로 설정
                answer_text = "답변이 없습니다."
            
            question_data.append({
                'question_text': question.question_text,
                'answer_text': answer_text,
            })
        return question_data

class ResponsesBeforeSerializer(serializers.Serializer):
    subtypes = SubtypeWithQuestionsSerializer(many=True)