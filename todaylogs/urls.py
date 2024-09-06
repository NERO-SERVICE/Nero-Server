from django.urls import path
from .views import (
    TodayListCreateView, 
    TodayDetailView, 
    QuestionListView, 
    SurveyResponseCreateView, 
    SideEffectResponseCreateView, 
    SelfRecordListCreateView,
    SurveyResponseListView,
    SideEffectResponseListView,
)

app_name = 'todaylogs'

urlpatterns = [
    path('', TodayListCreateView.as_view(), name='today-list-create'),
    path('<int:pk>/', TodayDetailView.as_view(), name='today-detail'),
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('survey/', SurveyResponseCreateView.as_view(), name='survey-response-create'),
    path('side_effect/', SideEffectResponseCreateView.as_view(), name='side-effect-response-create'),
    path('self_records/', SelfRecordListCreateView.as_view(), name='self-record-list-create'),
    path('survey/date/', SurveyResponseListView.as_view(), name='survey-response-list'),
    path('side_effect/date/', SideEffectResponseListView.as_view(), name='side-effect-response-list'),
]
