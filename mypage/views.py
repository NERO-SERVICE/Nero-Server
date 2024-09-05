from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import datetime
from .models import YearlyDoseLog, YearlySideEffectLog
from .serializers import YearlyDoseLogSerializer, YearlySideEffectLogSerializer

# 공통 매트릭스 생성 함수 (세로로 먼저 채우는 방식)
def generate_matrix(logs, start_date):
    # 7 * 53 매트릭스를 만들기 위한 기본 구조 (7일 * 53주)
    matrix = [[False] * 53 for _ in range(7)]
    first_weekday = start_date.weekday()  # 1월 1일의 요일 (월요일=0)

    # 로그를 매트릭스에 채워 넣음 (세로로 먼저)
    for log in logs:
        day_of_year = (log.date - start_date).days
        day_index = (day_of_year + first_weekday) % 7  # 요일에 해당하는 행 (세로)
        week_index = (day_of_year + first_weekday) // 7  # 주에 해당하는 열 (가로)

        # 매트릭스에 doseAction 또는 sideEffectAction 값을 삽입
        matrix[day_index][week_index] = log.doseAction if hasattr(log, 'doseAction') else log.sideEffectAction

    return matrix

# YearlyDoseLogView: YearlyDoseLog 데이터를 GET/POST 처리하는 APIView
class YearlyDoseLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year):
        start_date = datetime.date(year, 1, 1)  # 해당 연도의 시작일
        logs = YearlyDoseLog.objects.filter(owner=request.user, date__year=year).order_by('date')
        matrix = generate_matrix(logs, start_date)
        return Response(matrix)
    
    def post(self, request):
        serializer = YearlyDoseLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# YearlySideEffectLogView: YearlySideEffectLog 데이터를 GET/POST 처리하는 APIView
class YearlySideEffectLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year):
        start_date = datetime.date(year, 1, 1)  # 해당 연도의 시작일
        logs = YearlySideEffectLog.objects.filter(owner=request.user, date__year=year).order_by('date')
        matrix = generate_matrix(logs, start_date)
        return Response(matrix)
    
    def post(self, request):
        serializer = YearlySideEffectLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
