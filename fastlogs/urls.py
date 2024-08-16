from django.urls import path
from .views import SelfRecordListCreateView

app_name = 'fastlogs'

urlpatterns = [
    path('', SelfRecordListCreateView.as_view(), name='self-record-list-create'),
]