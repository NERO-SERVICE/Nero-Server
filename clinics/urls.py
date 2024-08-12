from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DrfClinicsViewSet, DrfDrugViewSet

app_name="clinics"

router = DefaultRouter()
router.register(r'', DrfClinicsViewSet, basename='clinics')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:clinicId>/', DrfClinicsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='clinic-detail'),
    path('<int:clinicId>/drugs/', DrfDrugViewSet.as_view({'get': 'list', 'post': 'create'}), name='clinic-drugs-list'),
    path('<int:clinicId>/drugs/<int:drugId>/', DrfDrugViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='clinic-drugs-detail'),
]
