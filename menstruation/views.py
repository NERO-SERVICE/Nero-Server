from rest_framework import generics
from rest_framework.views import APIView
from .models import Menstruation
from rest_framework.response import Response
from .serializers import MenstruationSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import date


class MenstruationListCreateView(generics.ListCreateAPIView):
    serializer_class = MenstruationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        year = self.request.query_params.get('year')
        if year:
            try:
                year = int(year)
                return Menstruation.objects.filter(owner=user, startDate__year=year)
            except ValueError:
                return Menstruation.objects.none()
        return Menstruation.objects.filter(owner=user)

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
        year = request.GET.get('year')

        if not year:
            return Response({"error": "Year parameter is required."}, status=400)

        try:
            year = int(year)
        except ValueError:
            return Response({"error": "Year parameter must be an integer."}, status=400)

        # 해당 연도의 첫 날과 마지막 날 계산
        first_day_of_year = date(year, 1, 1)
        last_day_of_year = date(year, 12, 31)

        # 생리 주기 데이터를 해당 연도 전체로 필터링
        cycles = Menstruation.objects.filter(
            owner=request.user,
            startDate__lte=last_day_of_year,
            endDate__gte=first_day_of_year,
        )

        serializer = MenstruationSerializer(cycles, many=True)
        return Response(serializer.data)