from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import YearlyDoseLog, YearlySideEffectLog
from .serializers import YearlyDoseLogSerializer, YearlySideEffectLogSerializer
import datetime

# 공통 매트릭스 생성 함수
def generate_matrix(logs, start_date):
    # 7 * 53 매트릭스를 만들기 위한 기본 구조
    matrix = [[False] * 7 for _ in range(53)]
    first_weekday = start_date.weekday()  # 1월 1일의 요일 (월요일=0)

    # 로그를 매트릭스에 채워 넣음
    for log in logs:
        day_of_year = (log.date - start_date).days
        week_index = (day_of_year + first_weekday) // 7
        day_index = (day_of_year + first_weekday) % 7
        matrix[week_index][day_index] = log.doseAction if hasattr(log, 'doseAction') else log.sideEffectAction

    return matrix

class YearlyDoseLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year):
        start_date = datetime.date(year, 1, 1)
        logs = YearlyDoseLog.objects.filter(owner=request.user, date__year=year).order_by('date')
        matrix = generate_matrix(logs, start_date)
        return Response(matrix)
    
    def post(self, request):
        serializer = YearlyDoseLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class YearlySideEffectLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year):
        start_date = datetime.date(year, 1, 1)
        logs = YearlySideEffectLog.objects.filter(owner=request.user, date__year=year).order_by('date')
        matrix = generate_matrix(logs, start_date)
        return Response(matrix)
    
    def post(self, request):
        serializer = YearlySideEffectLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
