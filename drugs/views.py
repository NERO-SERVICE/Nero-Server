from rest_framework import generics
from .models import DrugList, ClinicLog
from .serializers import DrugListSerializer, ClinicLogSerializer

class DrugListCreateView(generics.CreateAPIView):
    queryset = DrugList.objects.all()
    serializer_class = DrugListSerializer

class ClinicLogCreateView(generics.CreateAPIView):
    queryset = ClinicLog.objects.all()
    serializer_class = ClinicLogSerializer

class ClinicLogListView(generics.ListAPIView):
    queryset = ClinicLog.objects.all()
    serializer_class = ClinicLogSerializer
