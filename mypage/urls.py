from django.urls import path
from .views import YearlyLogView

app_name = 'mypage'

urlpatterns = [
    path('yearly-log/<int:year>/', YearlyLogView.as_view(), name='yearly-log'),
]