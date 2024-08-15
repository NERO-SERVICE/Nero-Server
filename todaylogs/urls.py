from django.urls import path
from .views import TodayListCreateView, TodayDetailView, SurveyUpdateView, SideEffectUpdateView, SelfRecordListCreateView

app_name='todaylogs'

urlpatterns = [
    path('', TodayListCreateView.as_view(), name='today-list-create'),
    path('<int:pk>/', TodayDetailView.as_view(), name='today-detail'),
    path('<int:pk>/survey/', SurveyUpdateView.as_view(), name='survey-update'),
    path('<int:pk>/side_effect/', SideEffectUpdateView.as_view(), name='side-effect-update'),
    path('<int:pk>/self_records/', SelfRecordListCreateView.as_view(), name='self-record-list-create'),
]
