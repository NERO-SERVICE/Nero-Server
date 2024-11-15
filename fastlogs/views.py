from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import DailyLog
from .serializers import DailyLogSerializer, DailyLogDateSerializer
from django.utils import timezone

class SelfRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = DailyLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')
        
        if not year or not month or not day:
            return DailyLog.objects.none()  # 필수 필터 조건이 없을 때 빈 쿼리셋 반환

        queryset = DailyLog.objects.filter(
            owner=self.request.user,
            date__year=year,
            date__month=month,
            date__day=day
        ).order_by('date')

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SelfRecordUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DailyLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailyLog.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class SelfRecordBulkUpdateView(generics.GenericAPIView):
    serializer_class = DailyLogSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        is_checked = request.data.get('is_checked', None)

        if not ids or is_checked is None:
            return Response({"detail": "Invalid data. 'ids' and 'is_checked' are required."}, status=status.HTTP_400_BAD_REQUEST)

        logs = DailyLog.objects.filter(owner=self.request.user, id__in=ids)
        if not logs.exists():
            return Response({"detail": "No matching logs found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        logs.update(is_checked=is_checked)
        return Response({"detail": "Logs updated successfully"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])

        if not ids:
            return Response({"detail": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        logs = DailyLog.objects.filter(owner=self.request.user, id__in=ids)
        if not logs.exists():
            return Response({"detail": "No matching logs found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        logs.delete()
        return Response({"detail": "Logs deleted successfully"}, status=status.HTTP_200_OK)

    
    
class SelfRecordUncheckedListView(generics.ListAPIView):
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
            date__day=day,
            is_checked=False
        ).order_by('date')
        
        return queryset
    
    
class SelfRecordDatesView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        queryset = DailyLog.objects.filter(owner=self.request.user)  # 로그인한 유저의 데이터만 필터
        
        if year:
            queryset = queryset.filter(date__year=year)
        if month:
            queryset = queryset.filter(date__month=month)
        
        if not year and not month:
            # 최근 12개월 데이터로 제한
            recent_months = timezone.now().date() - timezone.timedelta(days=365)
            queryset = queryset.filter(date__gte=recent_months)
        
        # distinct한 날짜 값만 추출
        dates = queryset.values_list('date', flat=True).distinct()

        return Response(dates)