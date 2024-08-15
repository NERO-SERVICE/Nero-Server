from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Today, SelfRecord, Question
from .serializers import TodaySerializer, SurveyResponseSerializer, SideEffectResponseSerializer, SelfRecordSerializer, TodayDetailSerializer, QuestionSerializer
from rest_framework.permissions import IsAuthenticated
from time import timezone

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
        if question_type:
            return Question.objects.filter(question_type=question_type)
        return super().get_queryset()

class SurveyResponseCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, today_id, question_id):
        today = Today.objects.get(pk=today_id, owner=request.user)
        question = Question.objects.get(pk=question_id)

        serializer = SurveyResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(today=today, question=question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SideEffectResponseCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, today_id, question_id):
        today = Today.objects.get(pk=today_id, owner=request.user)
        question = Question.objects.get(pk=question_id)

        serializer = SideEffectResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(today=today, question=question)
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
        today, created = Today.objects.get_or_create(owner=self.request.user, created_at=timezone.now().date())
        serializer.save(today=today)
