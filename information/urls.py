from django.urls import path
from .views import *

app_name = "information"

urlpatterns = [
    path('', ListInformationView.as_view(), name='list_informations'),
    path('create/', CreateInformationView.as_view(), name='create_information'),
    path('<int:id>/', RecentInformationsView.as_view(), name='get_information'),
    path('recent/', RecentInformationsView.as_view(), name='recent_informations'),
]
