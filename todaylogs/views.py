from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Today, SelfRecord, Question, Response as UserResponse, AnswerChoice, QuestionSubtype
from .serializers import SelfRecordSerializer, TodaySerializer, TodayDetailSerializer, QuestionSerializer, ResponseSerializer, QuestionSubtypeSerializer
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

        question_id = request.data.get('question_id')
        answer_id = request.data.get('answer_id')
        response_type = request.data.get('response_type')  # 'survey' 또는 'side_effect'로 구분

        if response_type not in ['survey', 'side_effect']:
            return Response({"error": "Invalid response type."}, status=status.HTTP_400_BAD_REQUEST)

        question = Question.objects.get(pk=question_id)
        answer = AnswerChoice.objects.get(pk=answer_id, question_subtype=question.question_subtype)

        serializer = ResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(today=today, question=question, answer=answer, response_type=response_type)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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