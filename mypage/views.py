from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import YearlyDoseLog, YearlySideEffectLog
from .serializers import YearlyDoseLogSerializer, YearlySideEffectLogSerializer

# YearlyDoseLogView: YearlyDoseLog 데이터를 GET/POST 처리하는 APIView
class YearlyDoseLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year):
        logs = YearlyDoseLog.objects.filter(owner=request.user, date__year=year).order_by('date')
        serializer = YearlyDoseLogSerializer(logs, many=True)
        return Response(serializer.data)

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
        logs = YearlySideEffectLog.objects.filter(owner=request.user, date__year=year).order_by('date')
        serializer = YearlySideEffectLogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = YearlySideEffectLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
