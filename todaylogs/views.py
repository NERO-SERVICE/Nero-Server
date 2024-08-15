from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Today, SelfRecord, Question
from .serializers import TodaySerializer, SurveyResponseSerializer, SideEffectResponseSerializer, SelfRecordSerializer, TodayDetailSerializer, QuestionSerializer
from rest_framework.permissions import IsAuthenticated

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
        today_id = self.kwargs['today_id']
        return SelfRecord.objects.filter(today_id=today_id, today__owner=self.request.user)

    def perform_create(self, serializer):
        today = Today.objects.get(pk=self.kwargs['today_id'], owner=self.request.user)
        serializer.save(today=today)
