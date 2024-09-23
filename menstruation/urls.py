from django.urls import path
from .views import MenstruationListCreateView, MenstruationRetrieveUpdateDestroyView, MenstruationCycleView

app_name = 'menstruation'

urlpatterns = [
    path('', MenstruationListCreateView.as_view(), name='menstruation-list-create'),
    path('<int:pk>/', MenstruationRetrieveUpdateDestroyView.as_view(), name='menstruation-detail'),
    path('cycles/', MenstruationCycleView.as_view(), name='menstruation-cycles'),
]

