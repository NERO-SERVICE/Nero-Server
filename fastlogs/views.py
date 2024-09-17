from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
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
            return Response({"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        logs = DailyLog.objects.filter(owner=self.request.user, id__in=ids)
        logs.update(is_checked=is_checked)

        return Response({"detail": "Logs updated successfully"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({"detail": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

        logs = DailyLog.objects.filter(owner=self.request.user, id__in=ids)
        logs.delete()

        return Response({"detail": "Logs deleted successfully"}, status=status.HTTP_200_OK)