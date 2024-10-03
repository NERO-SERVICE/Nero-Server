from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response as DRFResponse
from .models import Today, SelfRecord, Question, Response as UserResponse, AnswerChoice, QuestionSubtype, SurveyCompletion
from .serializers import SelfRecordSerializer, TodaySerializer, TodayDetailSerializer, QuestionSerializer, ResponseSerializer, QuestionSubtypeSerializer, SurveyCompletionSerializer
from django.db.models.functions import TruncDate

class TodayListCreateView(generics.ListCreateAPIView):
    serializer_class = TodaySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Today.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TodayDetailView(generics.RetrieveAPIView):
    queryset = Today.objects.all()
    serializer_class = TodayDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Today.objects.filter(owner=self.request.user)


class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        question_type = self.request.query_params.get('type', None)
        question_subtype = self.request.query_params.get('subtype', None)
        
        queryset = super().get_queryset()
        
        if question_type:
            queryset = queryset.filter(question_type__type_code=question_type)
        
        if question_subtype:
            queryset = queryset.filter(question_subtype__subtype_code=question_subtype)
        
        return queryset


class ResponseCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        today, created = Today.objects.get_or_create(
            owner=request.user,
            created_at__date=timezone.now().date(),
            defaults={'next_appointment_date': None}
        )

        response_type = request.data.get('response_type')  # 'survey' 또는 'side_effect'
        responses = request.data.get('responses')  # 응답 리스트

        if response_type not in ['survey', 'side_effect']:
            return Response({"error": "Invalid response type."}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(responses, list):
            return Response({"error": "Responses should be a list."}, status=status.HTTP_400_BAD_REQUEST)

        if not responses:
            return Response({"error": "No responses provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Extract subtypes from responses
        subtypes = set()
        for response_data in responses:
            question_id = response_data.get('question_id')
            try:
                question = Question.objects.get(pk=question_id)
                if question.question_subtype:
                    subtypes.add(question.question_subtype)
                else:
                    return Response({"error": "Question subtype is required."}, status=status.HTTP_400_BAD_REQUEST)
            except Question.DoesNotExist:
                return Response({"error": f"Question with id {question_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if len(subtypes) > 1:
            return Response({"error": "All responses must belong to the same subtype."}, status=status.HTTP_400_BAD_REQUEST)

        subtype = subtypes.pop()

        # Check if already completed
        if SurveyCompletion.objects.filter(today=today, response_type=response_type, question_subtype=subtype).exists():
            return Response({"error": "Survey for this subtype has already been completed today."}, status=status.HTTP_400_BAD_REQUEST)

        created_responses = []
        for response_data in responses:
            question_id = response_data.get('question_id')
            answer_id = response_data.get('answer_id')

            try:
                question = Question.objects.get(pk=question_id)
                answer = AnswerChoice.objects.get(pk=answer_id, question_subtype=question.question_subtype)
            except Question.DoesNotExist:
                return Response({"error": f"Question with id {question_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            except AnswerChoice.DoesNotExist:
                return Response({"error": f"AnswerChoice with id {answer_id} does not exist for the question's subtype."}, status=status.HTTP_400_BAD_REQUEST)

            response_instance = UserResponse(
                today=today,
                question=question,
                answer=answer,
                response_type=response_type
            )
            response_instance.save()
            created_responses.append(response_instance)

        # Create SurveyCompletion
        SurveyCompletion.objects.create(
            today=today,
            response_type=response_type,
            question_subtype=subtype
        )

        serializer = ResponseSerializer(created_responses, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class SelfRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = SelfRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')

        queryset = SelfRecord.objects.filter(
            today__owner=self.request.user,
            created_at__year=year,
            created_at__month=month,
            created_at__day=day
        )

        return queryset

    def perform_create(self, serializer):
        today, created = Today.objects.get_or_create(
            owner=self.request.user,
            created_at__date=timezone.now().date(),
            defaults={'next_appointment_date': None}
        )
        serializer.save(today=today)


class ResponseListView(generics.ListAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')
        response_type = self.request.query_params.get('response_type', 'all')  # 'survey', 'side_effect', 또는 'all'

        queryset = UserResponse.objects.filter(
            today__owner=self.request.user,
            today__created_at__year=year,
            today__created_at__month=month,
            today__created_at__day=day
        )

        if response_type in ['survey', 'side_effect']:
            queryset = queryset.filter(response_type=response_type)

        return queryset


class SelfRecordResponseListView(generics.ListAPIView):
    serializer_class = SelfRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')

        return SelfRecord.objects.filter(
            today__owner=self.request.user,
            created_at__year=year,
            created_at__month=month,
            created_at__day=day
        )
        
        
class RecordedDatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get('year')
        if not year:
            return Response({"error": "Year parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        response_type = request.query_params.get('response_type', 'all')  # 'survey', 'side_effect', 또는 'all'

        queryset = UserResponse.objects.filter(
            today__owner=request.user,
            today__created_at__year=year
        )

        if response_type in ['survey', 'side_effect']:
            queryset = queryset.filter(response_type=response_type)

        dates = queryset.annotate(date=TruncDate('today__created_at')).values_list('date', flat=True).distinct()
        date_strings = [date.isoformat() for date in dates]

        return Response(date_strings)


class SelfRecordRecordedDatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get('year')
        if not year:
            return Response({"error": "Year parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        dates = SelfRecord.objects.filter(
            today__owner=request.user,
            created_at__year=year
        ).annotate(date=TruncDate('created_at')).values_list('date', flat=True).distinct()

        date_strings = [date.isoformat() for date in dates]

        return Response(date_strings)
    

class QuestionSubtypeListView(generics.ListAPIView):
    serializer_class = QuestionSubtypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        type_code = self.request.query_params.get('type', None)
        queryset = QuestionSubtype.objects.all()

        if type_code:
            queryset = queryset.filter(type__type_code=type_code)

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        response_type = self.request.query_params.get('response_type', 'survey')
        context.update({'response_type': response_type})
        return context
    
class SurveyCompletionListView(generics.ListAPIView):
    serializer_class = SurveyCompletionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = Today.objects.filter(owner=self.request.user, created_at__date=timezone.now().date()).first()
        if not today:
            return SurveyCompletion.objects.none()
        return SurveyCompletion.objects.filter(today=today)
