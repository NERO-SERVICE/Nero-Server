from django.urls import path
from .views import (
    ListClinicsView,
    CreateClinicView,
    RetrieveClinicView,
    UpdateClinicView,
    DeleteClinicView
)

app_name = "clinics"

urlpatterns = [
    path('lists/', ListClinicsView.as_view(), name='list_clinics'),
    path('create/', CreateClinicView.as_view(), name='create_clinic'),
    path('<int:clinicId>/', RetrieveClinicView.as_view(), name='retrieve_clinic'),
    path('<int:clinicId>/update/', UpdateClinicView.as_view(), name='update_clinic'),
    path('<int:clinicId>/delete/', DeleteClinicView.as_view(), name='delete_clinic'),
]
