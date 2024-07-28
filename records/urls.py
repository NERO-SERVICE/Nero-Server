from django.urls import path
from .views import *

app_name = "records"

urlpatterns = [
    path('question/list/', QuestionListCreateView.as_view(), name='question-create'),
    path('servey/', ServeyLogCreateView.as_view(), name='log-create'),
    path('servey/list/', ServeyLogListView.as_view(), name='log-list'),
    path('symptomcare/list/', SymptomCareCreateView.as_view(), name='symptom-create'),
    path('symptom/', SymptomLogCreateView.as_view(), name='symptom-log-create'),
    path('symptom/list/', SymptomLogListView.as_view(), name='symptom-log-list'),
]