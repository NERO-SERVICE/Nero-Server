from django.urls import path
from .views import (
    ListClinicsView,
    RetrieveClinicView,
    UpdateClinicView,
    DeleteClinicView,
    ListDrugsView,
    RetrieveDrugView,
    UpdateDrugView,
    DeleteDrugView
)

app_name = "clinics"

urlpatterns = [
    path('', ListClinicsView.as_view(), name='list_clinics'),
    path('<int:clinicId>/', RetrieveClinicView.as_view(), name='retrieve_clinic'),
    path('<int:clinicId>/update/', UpdateClinicView.as_view(), name='update_clinic'),
    path('<int:clinicId>/delete/', DeleteClinicView.as_view(), name='delete_clinic'),
    path('<int:clinicId>/drugs/', ListDrugsView.as_view(), name='list_create_drugs'),
    path('<int:clinicId>/drugs/<int:drugId>/', RetrieveDrugView.as_view(), name='retrieve_drug'),
    path('<int:clinicId>/drugs/<int:drugId>/update/', UpdateDrugView.as_view(), name='update_drug'),
    path('<int:clinicId>/drugs/<int:drugId>/delete/', DeleteDrugView.as_view(), name='delete_drug'),
]
