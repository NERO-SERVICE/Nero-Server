from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import YearlyDoseLog, YearlySideEffectLog
import calendar

class YearlyLogView(APIView):
    def get(self, request, year, month):
        user = request.user
        log_type = request.query_params.get('type', 'all')
        
        dose_logs = YearlyDoseLog.objects.filter(owner=user, date__year=year, date__month=month)
        side_effect_logs = YearlySideEffectLog.objects.filter(owner=user, date__year=year, date__month=month)
        
        month_start, month_end = calendar.monthrange(year, month)

        adjusted_month_start = (month_start + 1) % 7 # 일요일 : index 0
        
        dose_check = {log.date.day: log.doseAction for log in dose_logs}
        side_effect_check = {log.date.day: log.sideEffectAction for log in side_effect_logs}
        
        # type에 따른 데이터 반환
        if log_type == 'all':
            response_data = {
                'date': f'{year}-{month}',
                'doseCheck': dose_check,
                'sideEffectCheck': side_effect_check,
                'monthStart': adjusted_month_start,
                'monthEnd': month_end
            }
        elif log_type == 'dose':
            response_data = {
                'date': f'{year}-{month}',
                'doseCheck': dose_check,
                'monthStart': adjusted_month_start,
                'monthEnd': month_end
            }
        elif log_type == 'side_effect':
            response_data = {
                'date': f'{year}-{month}',
                'sideEffectCheck': side_effect_check,
                'monthStart': adjusted_month_start,
                'monthEnd': month_end
            }
        else:
            return Response({"error": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response_data, status=status.HTTP_200_OK)