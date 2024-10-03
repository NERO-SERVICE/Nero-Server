from django.urls import path
from .views import (
    TodayListCreateView, 
    TodayDetailView, 
    QuestionListView, 
    ResponseCreateView,
    SelfRecordListCreateView,
    ResponseListView,
    SelfRecordResponseListView,
    RecordedDatesView,
    SelfRecordRecordedDatesView,
    QuestionSubtypeListView,
    SurveyCompletionListView,
    MypageSurveyCompletionListView,
    MypageSideEffectCompletionListView,
)

app_name = 'todaylogs'

urlpatterns = [
    path('', TodayListCreateView.as_view(), name='today-list-create'),
    path('<int:pk>/', TodayDetailView.as_view(), name='today-detail'),
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('response/', ResponseCreateView.as_view(), name='response-create'),
    path('self_records/', SelfRecordListCreateView.as_view(), name='self-record-list-create'),
    path('responses/', ResponseListView.as_view(), name='response-list'),
    path('self_record/date/', SelfRecordResponseListView.as_view(), name='self-record-response-list'),
    path('response/dates/', RecordedDatesView.as_view(), name='recorded-dates'),
    path('self_record/dates/', SelfRecordRecordedDatesView.as_view(), name='self-record-recorded-dates'),
    path('subtypes/', QuestionSubtypeListView.as_view(), name='subtype-list'),
    path('survey_completions/', SurveyCompletionListView.as_view(), name='survey-completion-list'),
    path('mypage_survey_completions/', MypageSurveyCompletionListView.as_view(), name='mypage-survey-completion-list'),
    path('mypage_side_effect_completions/', MypageSideEffectCompletionListView.as_view(), name='mypage-side-effect-completion-list'),
]
