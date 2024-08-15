from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Today, Survey, SideEffect, SelfRecord
from .serializers import TodaySerializer, SurveySerializer, SideEffectSerializer, SelfRecordSerializer, TodayDetailSerializer

class TodayListCreateView(generics.ListCreateAPIView):
    queryset = Today.objects.all()
    serializer_class = TodaySerializer

class TodayDetailView(generics.RetrieveAPIView):
    queryset = Today.objects.all()
    serializer_class = TodayDetailSerializer

class SurveyUpdateView(APIView):
    def put(self, request, pk):
        survey = Survey.objects.get(today_id=pk)
        serializer = SurveySerializer(survey, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SideEffectUpdateView(APIView):
    def put(self, request, pk):
        side_effect = SideEffect.objects.get(today_id=pk)
        serializer = SideEffectSerializer(side_effect, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SelfRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = SelfRecordSerializer

    def get_queryset(self):
        today_id = self.kwargs['pk']
        return SelfRecord.objects.filter(today_id=today_id)

    def perform_create(self, serializer):
        today = Today.objects.get(pk=self.kwargs['pk'])
        serializer.save(today=today)
