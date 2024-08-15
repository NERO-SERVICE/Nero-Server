from django.urls import path
from .views import (
    TodayListCreateView, 
    TodayDetailView, 
    QuestionListView, 
    SurveyResponseCreateView, 
    SideEffectResponseCreateView, 
    SelfRecordListCreateView
)

app_name='todaylogs'

urlpatterns = [
    path('', TodayListCreateView.as_view(), name='today-list-create'),
    path('<int:pk>/', TodayDetailView.as_view(), name='today-detail'),
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('<int:today_id>/survey/<int:question_id>/', SurveyResponseCreateView.as_view(), name='survey-response-create'),
    path('<int:today_id>/side_effect/<int:question_id>/', SideEffectResponseCreateView.as_view(), name='side-effect-response-create'),
    path('<int:today_id>/self_records/', SelfRecordListCreateView.as_view(), name='self-record-list-create'),
]
