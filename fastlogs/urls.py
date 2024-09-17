from django.urls import path
from .views import SelfRecordListCreateView, SelfRecordUpdateDeleteView, SelfRecordBulkUpdateView, SelfRecordUncheckedListView

app_name = 'fastlogs'

urlpatterns = [
    path('', SelfRecordListCreateView.as_view(), name='self-record-list-create'),
    path('<int:pk>/', SelfRecordUpdateDeleteView.as_view(), name='self-record-update-delete'),
    path('bulk/', SelfRecordBulkUpdateView.as_view(), name='self-record-bulk-update-delete'),
    path('unchecked/', SelfRecordUncheckedListView.as_view(), name='self-record-unchecked-list'),
]