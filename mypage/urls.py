from django.urls import path
from .views import YearlyLogView

app_name = 'mypage'

urlpatterns = [
    path('yearly-log/<int:year>/<int:month>/', YearlyLogView.as_view(), name='yearly-log'),
]
