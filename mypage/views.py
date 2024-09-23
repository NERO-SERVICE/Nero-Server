from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import YearlyDoseLog, YearlySideEffectLog
import calendar

class YearlyLogView(APIView):
    def get(self, request, year):
        user = request.user
        log_type = request.query_params.get('type', 'all')
        
        dose_logs = YearlyDoseLog.objects.filter(owner=user, date__year=year)
        side_effect_logs = YearlySideEffectLog.objects.filter(owner=user, date__year=year)
        
        # 월별 데이터를 저장할 딕셔너리
        monthly_data = {}
        
        for month in range(1, 13):
            month_dose_logs = dose_logs.filter(date__month=month)
            month_side_effect_logs = side_effect_logs.filter(date__month=month)
            
            month_start_day, month_end_day = calendar.monthrange(year, month)
            adjusted_month_start = (month_start_day + 1) % 7  # 일요일을 0으로 설정

            dose_check = {log.date.day: log.doseAction for log in month_dose_logs}
            side_effect_check = {log.date.day: log.sideEffectAction for log in month_side_effect_logs}
            
            # type에 따른 데이터 저장
            if log_type == 'all':
                monthly_data[month] = {
                    'date': f'{year}-{month}',
                    'doseCheck': dose_check,
                    'sideEffectCheck': side_effect_check,
                    'monthStart': adjusted_month_start,
                    'monthEnd': month_end_day
                }
            elif log_type == 'dose':
                monthly_data[month] = {
                    'date': f'{year}-{month}',
                    'doseCheck': dose_check,
                    'monthStart': adjusted_month_start,
                    'monthEnd': month_end_day
                }
            elif log_type == 'side_effect':
                monthly_data[month] = {
                    'date': f'{year}-{month}',
                    'sideEffectCheck': side_effect_check,
                    'monthStart': adjusted_month_start,
                    'monthEnd': month_end_day
                }
            else:
                return Response({"error": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(monthly_data, status=status.HTTP_200_OK)