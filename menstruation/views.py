from rest_framework import generics
from rest_framework.views import APIView
from .models import Menstruation
from rest_framework.response import Response
from .serializers import MenstruationSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import date
import calendar

class MenstruationListCreateView(generics.ListCreateAPIView):
    serializer_class = MenstruationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Menstruation.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MenstruationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenstruationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Menstruation.objects.filter(owner=self.request.user)

class MenstruationCycleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = int(request.GET.get('year'))
        month = int(request.GET.get('month'))

        # 해당 월의 첫 날과 마지막 날 계산
        first_day_of_month = date(year, month, 1)
        last_day_of_month = date(year, month, calendar.monthrange(year, month)[1])

        # 필터링 로직 수정
        cycles = Menstruation.objects.filter(
            owner=request.user,
            startDate__lte=last_day_of_month,
            endDate__gte=first_day_of_month,
        )

        serializer = MenstruationSerializer(cycles, many=True)
        return Response(serializer.data)