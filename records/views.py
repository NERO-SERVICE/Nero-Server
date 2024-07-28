from rest_framework import generics
from .models import QuestionList, ServeyLog, SymptomCare, SymptomLog
from .serializers import QuestionListSerializer, ServeyLogSerializer, SymptomCareSerializer, SymptomLogSerializer

class QuestionListCreateView(generics.CreateAPIView):
    queryset = QuestionList.objects.all()
    serializer_class = QuestionListSerializer

class ServeyLogCreateView(generics.CreateAPIView):
    queryset = ServeyLog.objects.all()
    serializer_class = ServeyLogSerializer

class ServeyLogListView(generics.ListAPIView):
    queryset = ServeyLog.objects.all()
    serializer_class = ServeyLogSerializer

class SymptomCareCreateView(generics.CreateAPIView):
    queryset = SymptomCare.objects.all()
    serializer_class = SymptomCareSerializer

class SymptomLogCreateView(generics.CreateAPIView):
    queryset = SymptomLog.objects.all()
    serializer_class = SymptomLogSerializer

class SymptomLogListView(generics.ListAPIView):
    queryset = SymptomLog.objects.all()
    serializer_class = SymptomLogSerializer