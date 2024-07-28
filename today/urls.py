from django.urls import path
from .views import TodayCreateView, TodayListView

app_name = 'today'

urlpatterns = [
    path('', TodayCreateView.as_view(), name='today-create'),
    path('list/', TodayListView.as_view(), name='today-list'),
]