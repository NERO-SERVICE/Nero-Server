from django.urls import path
from .views import DrugListCreateView, ClinicLogCreateView, ClinicLogListView

app_name = 'drugs'

urlpatterns = [
    path('', DrugListCreateView.as_view(), name='drug-create'),
    path('clinic-log/', ClinicLogCreateView.as_view(), name='clinic-log-create'),
    path('clinic-log/list/', ClinicLogListView.as_view(), name='clinic-log-list'),
]
