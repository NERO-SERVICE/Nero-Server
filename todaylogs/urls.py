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
    SelfRecordResponseListView,
    SurveyRecordedDatesView,
    SideEffectRecordedDatesView,
    SelfRecordRecordedDatesView,
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
    path('self_record/date/', SelfRecordResponseListView.as_view(), name='self-record-response-list'),
    path('survey/dates/', SurveyRecordedDatesView.as_view(), name='survey-recorded-dates'),
    path('side_effect/dates/', SideEffectRecordedDatesView.as_view(), name='side-effect-recorded-dates'),
    path('self_record/dates/', SelfRecordRecordedDatesView.as_view(), name='self-record-recorded-dates'),
]
