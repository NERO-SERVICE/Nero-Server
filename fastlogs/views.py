from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import DailyLog
from .serializers import DailyLogSerializer

class SelfRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = DailyLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')

        queryset = DailyLog.objects.filter(
            owner=self.request.user,
            date__year=year,
            date__month=month,
            date__day=day
        ).order_by('date')

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, date=timezone.now().date())
