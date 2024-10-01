from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import YearlyLog
from rest_framework.permissions import IsAuthenticated
import calendar

class YearlyLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year):
        user = request.user
        log_type = request.query_params.get('type', 'all')

        yearly_logs = YearlyLog.objects.filter(owner=user, date__year=year)
        
        if log_type in ['dose', 'side_effect']:
            yearly_logs = yearly_logs.filter(log_type=log_type)

        monthly_data = {}

        for month in range(1, 13):
            month_logs = yearly_logs.filter(date__month=month)
            _, month_end_day = calendar.monthrange(year, month)
            adjusted_month_start = (month_logs.first().date.weekday() + 1) % 7 if month_logs.exists() else 0  # 일요일이 0

            log_data = {
                'doseCheck': {},
                'sideEffectCheck': {}
            }

            for log in month_logs:
                if log.log_type == 'dose':
                    log_data['doseCheck'][log.date.day] = log.action
                elif log.log_type == 'side_effect':
                    log_data['sideEffectCheck'][log.date.day] = log.action

            if log_type == 'all':
                monthly_data[month] = {
                    'date': f'{year}-{month}',
                    'doseCheck': log_data['doseCheck'],
                    'sideEffectCheck': log_data['sideEffectCheck'],
                    'monthStart': adjusted_month_start,
                    'monthEnd': month_end_day
                }
            elif log_type == 'dose':
                monthly_data[month] = {
                    'date': f'{year}-{month}',
                    'doseCheck': log_data['doseCheck'],
                    'monthStart': adjusted_month_start,
                    'monthEnd': month_end_day
                }
            elif log_type == 'side_effect':
                monthly_data[month] = {
                    'date': f'{year}-{month}',
                    'sideEffectCheck': log_data['sideEffectCheck'],
                    'monthStart': adjusted_month_start,
                    'monthEnd': month_end_day
                }
            else:
                return Response({"error": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(monthly_data, status=status.HTTP_200_OK)