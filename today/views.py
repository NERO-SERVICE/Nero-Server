from rest_framework import generics
from .serializers import TodaySerializer
from .models import Today

# Create your views here.
class TodayCreateView(generics.CreateAPIView):
    queryset = Today.objects.all()
    serializer_class = TodaySerializer

class TodayListView(generics.ListAPIView):
    queryset = Today.objects.all()
    serializer_class = TodaySerializer