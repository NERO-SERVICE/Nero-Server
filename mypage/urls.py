from django.urls import path
from .views import YearlyDoseLogView, YearlySideEffectLogView

app_name = 'mypage'

urlpatterns = [
    path('yearly-dose-log/<int:year>/', YearlyDoseLogView.as_view(), name='yearly-dose-log'),
    path('yearly-dose-log/', YearlyDoseLogView.as_view(), name='yearly-dose-log-post'),
    path('yearly-side-effect-log/<int:year>/', YearlySideEffectLogView.as_view(), name='yearly-side-effect-log'),
    path('yearly-side-effect-log/', YearlySideEffectLogView.as_view(), name='yearly-side-effect-log-post'),
]
